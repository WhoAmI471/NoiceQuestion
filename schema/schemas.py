from pydantic import BaseModel

class UserStats(BaseModel):
    user_id: str
    training: int
    easy: int
    medium: int
    hard: int

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        user_id = data.pop('user_id')  # Извлекаем user_id из словаря
        return cls(user_id=user_id, **data)  # Создаем экземпляр класса с остальными данными

        