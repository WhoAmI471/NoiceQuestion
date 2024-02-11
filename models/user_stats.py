from pydantic import BaseModel

class UserStats(BaseModel):
    user_id: str
    training: int
    easy: int
    medium: int
    hard: int