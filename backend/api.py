import os
import requests
import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from typing import Dict, Optional
from urllib.parse import urlencode

app = FastAPI(root_path='/api/v1')

app.add_middleware(SessionMiddleware, secret_key=os.environ["FASTAPI_SESSION_SECRET_KEY"])
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080"],
  allow_methods=["GET", "POST", "OPTIONS"],
  allow_headers=["Content-Type", "Authorization"],
)

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
  return RedirectResponse(url=auth_url)

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

  request.session["user"] = {
    "name": user_info["name"],
    "email": user_info["email"],
    "picture": user_info.get("picture")
  }

  return RedirectResponse(url="/api/v1/profile")

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

@app.get("/chat")
async def chat(messages: Dict, request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  assistant_reply = {"role": "assistant", "content": "Here is a response based on your messages."}
  videos = [
    {"yt_link": "https://youtube.com/example1", "title": "Example Video 1", "description": "Description of video 1"},
    {"yt_link": "https://youtube.com/example2", "title": "Example Video 2", "description": "Description of video 2"},
  ]
  return {"reply": assistant_reply, "videos": videos}

@app.post("/library")
async def add_to_library(video: Dict, request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  return {"message": "Video added to library", "video": video}

@app.get("/library")
async def get_library(request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  library = [
    {"yt_link": "https://youtube.com/example1", "title": "Example Video 1"},
    {"yt_link": "https://youtube.com/example2", "title": "Example Video 2"},
  ]
  return {"videos": library}

@app.get("/watch")
async def watch(yt_link: str, request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  video_details = {
    "outline": "# Video Outline\n- Introduction\n- Main Content\n- Summary",
    "quiz": [
      {"question": "What is the main topic?", "answer": "The main topic is X."},
      {"question": "How is it implemented?", "answer": "It is implemented using Y."}
    ]
  }
  return video_details

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("api:app", host="localhost", port=8081, reload=True)
