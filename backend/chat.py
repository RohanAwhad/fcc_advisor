import google.generativeai as genai
import json
import googleapiclient
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Configure YouTube API
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=os.environ["YOUTUBE_DEV_KEY"])

def load_memory():
    try:
        with open('user_memory.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_memory(memory):
    with open('user_memory.json', 'w') as f:
        json.dump(memory, f, indent=2)

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
            "yt_link": f"https://www.youtube.com/watch?v={item['id']}",
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "thumbnail": item['snippet']['thumbnails']['high']['url'],
        }
        videos.append(video)
    return videos

def summarize_conversation(conversation):
    prompt = f"Summarize the following conversation concisely:\n{conversation}"
    response = model.generate_content(prompt)
    return response.text

def extract_keywords(conversation):
    prompt = f"""Identify and extract the most relevant keywords from this conversation that can be effectively used as search queries for educational videos on YouTube. Focus on terms and phrases that represent core topics, skills, tools, or concepts discussed in the conversation.
    Conversation :{conversation}"""
    response = model.generate_content(prompt)
    return response.text

async def final_bot_reply(conversation, videos):
    prompt = f"""Based on the given conversation and video suggestions form a reply which can ask the user for future clarification while also mentioning that it can refer the videos given. Reply should be less than 50 words.
    Conversation :{conversation}
    Video Suggestions: {videos}"""
    response = model.generate_content(prompt)
    return response.text

async def chat_with_user(user_email, message):
    memory = load_memory()
    if user_email not in memory:
        memory[user_email] = {"memory": ""}
    
    conversation = "System Prompt: The user wants to learn something, help them narrow down what they want to learn. Reply should be less than 100 words.\n"
    conversation += f"User: {message}\n"
    response = model.generate_content(conversation + memory[user_email]["memory"])
    conversation += f"Chatbot: {response.text}\n"

    keyword = extract_keywords(conversation)
    videos = await search_youtube_videos(keyword)
    final_ans = await final_bot_reply(conversation,  json.dumps(videos))

    # summary = summarize_conversation(conversation)
    memory[user_email]["memory"] = keyword
    save_memory(memory)
    print("output", response.text, json.dumps(videos[0]))

    return {"reply":final_ans, "videos":videos}







    

