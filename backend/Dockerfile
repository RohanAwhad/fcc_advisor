FROM python:3.12
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install yt-dlp
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
#CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
CMD ["python", "video_analyzer.py"]
