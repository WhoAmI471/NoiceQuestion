from pathlib import Path
from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from models.user_stats import UserStats
from config.database import user_stats_collection
import os
import shutil

router = APIRouter()

# GET Request Method to retrieve user statistics
@router.get("/user-stats/{user_id}")
async def get_user_stats(user_id: str):
    user_stats = user_stats_collection.find_one({"user_id": user_id})
    if user_stats:
        user_stats["_id"] = str(user_stats["_id"])  # Convert ObjectId to string
        return user_stats
    else:
        initial_stats = {"user_id": user_id, "training": 0, "easy": 0, "medium": 0, "hard": 0}
        user_stats_collection.insert_one(initial_stats)
        initial_stats["_id"] = str(initial_stats["_id"])  # Convert ObjectId to string
        return initial_stats

# POST Request Method to update user statistics
@router.post("/user-stats/{user_id}")
async def update_user_stats(user_id: str, stats: UserStats):
    user_stats_collection.find_one_and_update({"user_id": user_id}, {"$set": stats.model_dump()})

# GET Request Method to serve video
@router.get("/video/{video_id}")
async def get_video(video_id: str):
    video_path = f"video/{video_id}.mp4"  # Укажите путь к видеофайлам на сервере
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        return {"error": "Video not found"}


# POST Request Method to upload video
@router.post("/video")
async def upload_video(video: UploadFile = File(...)):
    video_path = f"video/{video.filename}"  # Укажите путь для сохранения видеофайла на сервере
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {"message": "Video uploaded successfully"}
