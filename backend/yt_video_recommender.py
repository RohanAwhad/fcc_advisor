import os
import googleapiclient

# Configure YouTube API
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=os.environ["YOUTUBE_DEV_KEY"])
async def search_youtube_videos(query: str, max_results: int = 3):
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        channelId="UC8butISFwT-Wl7EV0hUK0BQ",  # freeCodeCamp channel ID
        maxResults=max_results
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get("items", [])]
    if not video_ids:
        return []

    videos = []
    videos_response = youtube.videos().list(
        part="snippet",
        id=",".join(video_ids)
    ).execute()
    for item in videos_response.get("items", []):
    # for item in search_response.get("items", []):
        video = {
            "video_id": item['id'],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "thumbnail_url": item['snippet']['thumbnails']['high']['url'],
        }
        videos.append(video)
    return videos
