import requests
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from telegram import Bot
import time
import os
import random
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Telegram Setup
TELEGRAM_TOKEN = "7319427084:AAGPm-poL8cUQsvmTIhI2j9xAIlEm8CXcF0"
CHAT_ID = "5015166670"
bot = Bot(TELEGRAM_TOKEN)

# YouTube API Setup
YOUTUBE_API_KEY = "AIzaSyByO9jsSHx_TeNRF9n1A7KzGcWflzqyyig"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Stock Videos (Render ke disk se)
stock_videos = ["stock_footage1.mp4", "stock_footage2.mp4", "stock_footage3.mp4", "stock_footage4.mp4", "stock_footage5.mp4"]

# Successful Patterns
successful_patterns = []

def get_trending_topic():
    topics = ["AI Trading Secrets", "AI Crypto Hacks", "Finance with AI", "AI Stock Tips", "AI Money Tricks"]
    topic = random.choice(topics)
    bot.send_message(chat_id=CHAT_ID, text=f"Trending Topic: {topic}")
    return topic

def generate_script(topic):
    hooks = ["Millionaires use THIS!", "Secrets YOU need!", "Boost profits NOW!", "AI hacks revealed!", "Get rich with THIS!"]
    hook = random.choice(hooks)
    script = f"{hook} Learn {topic} to skyrocket your income fast!"
    bot.send_message(chat_id=CHAT_ID, text=f"Script: {script}")
    return script

def generate_voice(script):
    tts = gTTS(script)
    tts.save("voice.mp3")
    bot.send_message(chat_id=CHAT_ID, text="Voice generated!")
    return "voice.mp3"

def create_video(voice_path, topic):
    stock_file = random.choice(stock_videos)
    clip = VideoFileClip(stock_file).subclip(0, 30)
    audio = AudioFileClip(voice_path)
    text = TextClip(topic, fontsize=30, color='white', bg_color='black').set_duration(30)
    final_clip = CompositeVideoClip([clip.set_audio(audio), text.set_pos('center')])
    final_clip.write_videofile("output.mp4", codec="libx264")
    bot.send_message(chat_id=CHAT_ID, text="Video created!")
    return "output.mp4"

def upload_video(video_path, title, description, tags):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "27"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(video_path)
    )
    response = request.execute()
    bot.send_message(chat_id=CHAT_ID, text="Video uploaded!")
    return response['id']

def analyze_and_improve(video_id, topic, title, tags):
    time.sleep(86400)  # Check after 24 hours
    stats = youtube.videos().list(part="statistics", id=video_id).execute()
    views = int(stats['items'][0]['statistics']['viewCount'])
    bot.send_message(chat_id=CHAT_ID, text=f"Views: {views}")
    if views > 1000:
        successful_patterns.append({"topic": topic, "title": title, "tags": tags})
        bot.send_message(chat_id=CHAT_ID, text="Pattern saved!")
    elif views < 100:
        new_title = f"Updated: {title}"
        upload_video("output.mp4", new_title, description, tags + ["trending", "viral"])

# Main Loop (3 shorts/day)
while True:
    topic = get_trending_topic()
    script = generate_script(topic)
    voice_path = generate_voice(script)
    if voice_path:
        video_path = create_video(voice_path, topic)
        if video_path:
            title = f"{topic} - Boost Your Income!"
            description = f"Master {topic} with AI! Subscribe now!"
            tags = ["AI", "Finance", "Trading", topic, "2025"]
            video_id = upload_video(video_path, title, description, tags)
            if video_id:
                analyze_and_improve(video_id, topic, title, tags)
    time.sleep(28800)  # 8 hours = 3 uploads/day
