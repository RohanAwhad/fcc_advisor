import os
import copy
import requests
import jwt
import yaml
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from typing import Dict, Optional, List
from urllib.parse import urlencode
from pydantic import BaseModel, Field

import db
import utils
import structured_llm_output as llm
import yt_video_recommender

app = FastAPI(root_path='/api/v1')

app.add_middleware(SessionMiddleware, secret_key=os.environ["FASTAPI_SESSION_SECRET_KEY"])
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080"],
  allow_methods=["GET", "POST", "OPTIONS"],
  allow_headers=["Content-Type", "Authorization"],
)
db.check_and_create_tables()

client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = "http://localhost:8080/api/v1/auth/google/callback"

@app.get("/login")
async def login(request: Request):
  auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
  auth_params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": "openid email profile",
    "access_type": "offline",
    "prompt": "consent"
  }
  auth_url = f"{auth_base_url}?{urlencode(auth_params)}"
  return {'auth_url': auth_url}

@app.get("/auth/google/callback")
async def auth_google_callback(request: Request):
  auth_code = request.query_params.get("code")
  token_url = "https://oauth2.googleapis.com/token"
  token_data = {
    "code": auth_code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
  }
  token_response = requests.post(token_url, data=token_data)
  token_response_data = token_response.json()
  access_token = token_response_data['access_token']
  
  user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  headers = {"Authorization": f"Bearer {access_token}"}
  user_info_response = requests.get(user_info_url, headers=headers)
  user_info = user_info_response.json()

  if not db.check_user_by_email(user_info['email']):
    # add to db
    db.create_user(db.User(user_id=user_info['id'], name=user_info['name'], email=user_info['email']))

  request.session["user"] = {
    "user_id": user_info['id'],
    "name": user_info["name"],
    "email": user_info["email"],
    "picture": user_info.get("picture")
  }

  return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
  request.session.pop("user", None)
  return JSONResponse({"message": "Successfully logged out"})

def get_current_user(request: Request) -> Optional[Dict]:
  return request.session.get("user")

@app.get("/profile")
async def profile(request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  return user


class Message(BaseModel):
  role: str = Field(..., desc='user, system, or assistant only')
  content: str = Field(..., desc='message content')

class VideoIn(BaseModel):
  video_id: str
  url: str
  description: str
  title: str
  thumbnail_url: str

class Video(VideoIn):
  outline: str | None = None

class ChatOut(BaseModel):
  reply: Message = Field(..., desc='assistant reply')
  videos: List[Video] = Field(..., desc='video objects')

@app.post("/recommend_videos", response_model=ChatOut)
async def chat(messages: list[Message], request: Request):
  '''
  - based on latest messages generate search query 
  - get a list of videos that would are related to the chat
  - add title and description at the end of the messages to as context
  - now with the new messages list generate an assistant reply
  '''
  with open('prompts/recommend_videos_chat.txt', 'r') as f:
    chat_sys_prompt = f.read()
  with open('prompts/recommend_videos_keyword_gen.txt', 'r') as f:
    keyword_gen_sys_prompt = f.read()

  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")

  class SearchQuery(BaseModel):
    scratch_pad: str = Field(desc='a scratchpad for you to layout your thoughts, before writing down the query')
    query: str = Field(desc='search query 3-8 words')

  res = llm.run('gemini-1.5-flash', messages=copy.deepcopy([Message(role='system', content=keyword_gen_sys_prompt),] + messages), response_model=SearchQuery, provider='google', max_retries=3)
  videos_list = await yt_video_recommender.search_youtube_videos(res.query)
  print(videos_list)
  videos_list = [VideoIn.model_validate(x) for x in videos_list]
  recommended_yt_videos = yaml.safe_dump([{'title': x.title, 'description': x.description} for x in videos_list])
  messages[-1].content += f'\n\nRecommended Youtube Videos:\n```yaml\n{recommended_yt_videos}\n```'

  final_message = [f'{m.role.lower()}:\n{m.content}\n\n---\n' for m in [Message(role='system', content=chat_sys_prompt),]+messages] + ['assitant:',]
  final_message = ''.join(final_message)
  model = genai.GenerativeModel(model_name='gemini-1.5-flash')
  response = model.generate_content([final_message,], request_options={"timeout": 600})
  llm_res = response.text

  assistant_reply = {"role": "assistant", "content": llm_res}
  return {"reply": assistant_reply, "videos": videos_list}



@app.post("/library", status_code=201)
async def add_to_library(video: VideoIn, request: Request):
  '''
  - should add the video to video table
  - then add the videoid, user id to library table 
  - add the video_id to worker process for outline and quiz analysis questions
  '''
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")

  # Check if the video already exists in the database
  existing_video: Optional[db.Video] = db.read_video(video.video_id)
  # Create the video if it doesn't exist
  if not existing_video:
    db.create_video(db.Video(
      video_id=video.video_id,
      url=video.url,
      description=video.description,
      title=video.title,
      thumbnail_url=video.thumbnail_url,
    ))

  db.create_library(db.Library(user['user_id'], video.video_id))
  # TODO: add the video_id to the worker queue


class LibGetOut(BaseModel):
  response: list[Video]
@app.get("/library", response_model=LibGetOut)
async def get_library(request: Request):
  '''
  - get list of video objects in the given users library
  '''
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")

  library = db.get_videos_by_user(user['user_id'])
  return {"response": library}


@app.delete("/library/{video_id}", status_code=204)
async def remove_from_library(video_id: str, request: Request):
  '''
  - remove the video from the user's library
  '''
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  if not db.check_video_in_library(user['user_id'], video_id):
    raise HTTPException(status_code=404, detail="Video not found in library")
  
  db.delete_library(user['user_id'], video_id)
  return JSONResponse({'message': 'video successfully removed from user library'}, status_code=204)  # No Content



class QuizQuestion(BaseModel):
  question: str
  answer: str

class VideoDetails(BaseModel):
  outline: str = Field(..., desc="Outline of the video")
  quiz: list[QuizQuestion] = Field(..., desc="List of quiz questions and answers")

@app.get("/watch", response_model=VideoDetails)
async def watch(video_id: str, request: Request):
  user = get_current_user(request)
  if not user: raise HTTPException(status_code=401, detail="Unauthorized")

  quizzes = db.read_quizzes_by_video(video_id)
  video = db.read_video(video_id)
  video_details = {
    "outline": video.outline,
    "quiz": [{"question":q.question, "answer": q.answer} for q in quizzes]
  }
  return video_details

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("api:app", host="localhost", port=8081, reload=True)
