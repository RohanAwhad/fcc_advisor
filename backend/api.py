import os
import requests
import jwt

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from typing import Dict, Optional

app = FastAPI(root_path='/api/v1')

# Middleware for sessions and CORS
app.add_middleware(SessionMiddleware, secret_key=os.environ["FASTAPI_SESSION_SECRET_KEY"])
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080"],
  allow_methods=["GET", "POST", "OPTIONS"],
  allow_headers=["Content-Type", "Authorization"],
)

# OAuth configuration
oauth = OAuth()
oauth.register(
  name="google",
  client_id=os.environ["GOOGLE_CLIENT_ID"],
  client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
  server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
  client_kwargs={"scope": "openid email profile"}
)

@app.get("/login")
async def login(request: Request):
  redirect_uri = request.url_for("auth_google_callback")
  return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def auth_google_callback(request: Request):
  token = await oauth.google.authorize_access_token(request)
  id_token = token.get("id_token")
  user_info = jwt.decode(id_token, options={"verify_signature": False})

  # Store user in session
  request.session["user"] = {
    "name": user_info["name"],
    "email": user_info["email"],
    "picture": user_info.get("picture")
  }

  return RedirectResponse(url="/api/profile")

@app.get("/logout")
async def logout(request: Request):
  request.session.pop("user", None)
  return JSONResponse({"message": "Successfully logged out"})

# Helper function to get the logged-in user
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
  
  # Mock assistant response and video recommendations
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
  
  # Simulating adding video to the library
  return {"message": "Video added to library", "video": video}

@app.get("/library")
async def get_library(request: Request):
  user = get_current_user(request)
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  
  # Simulating retrieving the user's library
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
  
  # Simulating video details
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
