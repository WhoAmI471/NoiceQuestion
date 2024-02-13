from pathlib import Path
from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from models.user_stats import UserStats
from config.database import user_stats_collection
import os
import shutil

router = APIRouter()


# GET Request Method to retrieve all user statistics
@router.get("/user-stats", tags=["User Stats"])
async def get_all_user_stats():
    """
    Retrieve all user statistics.
    """
    all_user_stats = []
    for user_stats in user_stats_collection.find():
        user_stats["_id"] = str(user_stats["_id"])  # Convert ObjectId to string
        all_user_stats.append(user_stats)
    return {"user_stats": all_user_stats}


# GET Request Method to retrieve user statistics
@router.get("/user-stats/{user_id}", tags=["User Stats"])
async def get_user_stats(user_id: str):
    """
    Retrieve user statistics by user_id.
    """
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
@router.post("/user-stats/{user_id}", tags=["User Stats"])
async def update_user_stats(user_id: str, stats: UserStats):
    """
    Update user statistics by user_id.
    """
    user_stats_collection.find_one_and_update({"user_id": user_id}, {"$set": stats.model_dump()})


# PUT Request Method to update specific user statistic
@router.put("/user-stats/{user_id}", tags=["User Stats"])
async def update_specific_user_stat(user_id: str, stat_name: str, new_value: int):
    """
    Update a specific user statistic by user_id and stat_name.
    """
    allowed_stat_names = ["training", "easy", "medium", "hard"]
    if stat_name in allowed_stat_names:
        user_stats_collection.find_one_and_update({"user_id": user_id}, {"$set": {stat_name: new_value}})
        return {"message": f"{stat_name} statistic updated successfully"}
    else:
        return {"error": "Invalid stat name. Allowed stat names are 'training', 'easy', 'medium', 'hard'"}


# DELETE Request Method to delete a specific user statistic
@router.delete("/user-stats/{user_id}", tags=["User Stats"])
async def delete_user_stat(user_id: str):
    """
    Delete a specific user statistic by user_id.
    """
    result = user_stats_collection.delete_one({"user_id": user_id})
    if result.deleted_count == 1:
        return {"message": "User statistic deleted successfully"}
    else:
        return {"error": "User statistic not found"}



# GET Request Method to serve video
@router.get("/video/{video_id}", tags=["Video"])
async def get_video(video_id: str):
    """
    Get a video by video_id.
    """
    video_path = f"video/{video_id}.mp4"  # Укажите путь к видеофайлам на сервере
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        return {"error": "Video not found"}


# POST Request Method to upload video
@router.post("/video", tags=["Video"])
async def upload_video(video: UploadFile = File(...)):
    """
    Upload a video file.
    """
    video_path = f"video/{video.filename}"  # Укажите путь для сохранения видеофайла на сервере
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {"message": "Video uploaded successfully"}


# DELETE Request Method to delete video
@router.delete("/video/{video_id}", tags=["Video"])
async def delete_video(video_id: str):
    """
    Delete a video by video_id.
    """
    video_path = f"video/{video_id}.mp4"  # Укажите путь к видеофайлу на сервере
    if os.path.exists(video_path):
        os.remove(video_path)
        return {"message": "Video deleted successfully"}
    else:
        return {"error": "Video not found"}


# GET Request Method to get list of videos with their sizes
@router.get("/videos", tags=["Video"])
async def get_videos_list():
    """
    Get a list of videos with their sizes.
    """
    video_dir = Path("video")  # Укажите путь к директории с видеофайлами
    video_list = []
    for video_file in video_dir.iterdir():
        if video_file.is_file():
            video_list.append({
                "filename": video_file.name,
                "size": video_file.stat().st_size  # Размер файла в байтах
            })
    return {"videos": video_list}
