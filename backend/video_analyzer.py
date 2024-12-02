import time
import re
import subprocess
import hashlib
import os
from urllib.parse import urlparse
from google.cloud import storage
import google.generativeai as genai
from jinja2 import Template
from pydantic import BaseModel, ValidationError
import yaml
import tomlkit
import json


BUCKET_NAME = "fcc-advisor-bucket-1"
CREDENTIALS_FILE = "gcs_obj_creation_sa.json"

class QnA(BaseModel):
  question: str
  answer: str

class ResponseStruct(BaseModel):
  outline: str
  quiz: list[QnA]



def run(yt_link: str) -> None:
  url_hash = hashlib.md5(yt_link.encode()).hexdigest()
  temp_dir = f"/tmp/{url_hash}"
  os.makedirs(temp_dir, exist_ok=True)
  os.makedirs(f"{temp_dir}/chunks", exist_ok=True)

  # Use yt-dlp to get the filename
  result = subprocess.run(
      ["yt-dlp", "--print", "filename", "-o", f"{temp_dir}/full_video.%(ext)s", yt_link],
      capture_output=True,
      text=True,
      check=True
  )
  full_video_path = result.stdout.strip()
  print('yt-dlp path:', full_video_path)
  # Download YouTube video
  subprocess.run(["yt-dlp", "-o", full_video_path, yt_link], check=True)

  # Get video duration
  duration_output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_video_path])
  duration = float(duration_output)

  # Split video into chunks
  chunk_duration = 40 * 60  # 40 minutes in seconds
  overlap = 5 * 60  # 5 minutes overlap in seconds
  outline, quiz = None, None
  
  # TODO: delete this. refactor. should be done async
  uploaded_files = ["files/9mrh9xq2q119", "files/9rup881ton4o"]
  for i, start_time in enumerate(range(0, int(duration), chunk_duration - overlap)):
    end_time = min(start_time + chunk_duration, duration)
    output_path = f"{temp_dir}/chunks/clip_{i}.mp4"
    
    if not os.path.exists(output_path):
      subprocess.run([
        "ffmpeg",
        "-i", full_video_path,
        "-ss", str(start_time),
        "-to", str(end_time),
        "-c", "copy",
        output_path
      ], check=True)
    #upload_to_gcs(BUCKET_NAME, output_path, destination_blob_name, credentials_file)
    #video_file = upload_to_gemini(output_path)
    for f in genai.list_files():
      if f.name == uploaded_files[i]:
        video_file = f
        break

    outline, quiz = ask_gemini(video_file, outline, json.dumps([x.model_dump() for x in quiz]) if quiz else None)
    if end_time >= duration:
      print('Final Outline:')
      print(outline)
      print('Quiz:')
      print(yaml.dumps([x.model_dump() for x in quiz]), flush=True)
      break

def upload_to_gemini(file_path):
  # Check whether the file is ready to be used.
  video_file = genai.upload_file(path=file_path)
  print('Uploading file')
  while video_file.state.name == "PROCESSING":
      print('.')
      time.sleep(10)
      video_file = genai.get_file(video_file.name)

  if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)
  return video_file


def ask_gemini(video_file, outline=None, quiz_questions=None):
  # load prompts from prompts/video_analyzer.txt as jinja2 template and pass it outline and quiz_questions
  with open("prompts/video_analyzer.txt") as file:
    template_content = file.read()

  template = Template(template_content)
  formatted_prompt = template.render(outline=outline, quiz_questions=quiz_questions)


  # Choose a Gemini model.
  model = genai.GenerativeModel(model_name="gemini-1.5-flash")
  print("Making LLM inference request...", flush=True)
  response = model.generate_content([video_file, formatted_prompt], request_options={"timeout": 600})
  llm_res = response.text
  ptrn = re.compile(r"```json(.*?)```", re.DOTALL)
  match = re.search(ptrn, llm_res)
  if match:
    try:
      res_dict = json.loads(match.group(1))
      if isinstance(res_dict, dict): ret = ResponseStruct.model_validate(res_dict)
      elif isinstance(res_dict, list): ret = [ResponseStruct.model_validate(x) for x in res_dict]
      else: raise Exception(f"Shouldn't have reached here. Expected type of dict or list, but got {type(res_dict)}")
      return ret.outline, ret.quiz

    except ValidationError as e:
      print("Pydantic Validation Error:", e)
      print(llm_res)
    except yaml.YAMLError as e:
      print("YAML parsing error:", e)
      print(llm_res)
    except Exception as e:
      print("Error:", e)
      print(llm_res)

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file):
  # Initialize the Google Cloud Storage client with the credentials
  storage_client = storage.Client.from_service_account_json(credentials_file)

  # Get the target bucket
  bucket = storage_client.bucket(bucket_name)

  # Upload the file to the bucket
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(source_file_path)

  print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")




# Example usage
if __name__ == '__main__':
  print("My files:")
  for f in genai.list_files():
      print("  ", f.name)

  run('https://www.youtube.com/watch?v=lG7Uxts9SXs')
  #SOURCE_FILE_PATH = "/tmp/2fe387470299859be578fe0a78329ba9/chunks/clip_0.mp4"
  #DESTINATION_BLOB_NAME = "2fe387470299859be578fe0a78329ba9/clip_0.mp4"
  #upload_to_gcs(BUCKET_NAME, SOURCE_FILE_PATH, DESTINATION_BLOB_NAME, CREDENTIALS_FILE)
