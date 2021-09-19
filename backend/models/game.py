from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class GameSchema(BaseModel):
    title: str = Field(None, title="Game title", max_length=60)
    description: Optional[str] = Field(None, title="Game description", max_length=300)
    published_date: Optional[date] = Field(None, title="Published date")

    class Config:
        schema_extra = {
            "example": {
                "title": "Battle Brothers",
                "description": "Battle Brothers is a turn based game which has"
                " you leading a mercenary company in a gritty, low-power, "
                "medieval fantasy world.",
                "published_date": date(2015, 4, 27),
            }
        }


class UpdateGameModel(BaseModel):
    title: Optional[str] = Field(None, title="Game title", max_length=60)
    description: Optional[str] = Field(None, title="Game description", max_length=300)
    published_date: Optional[date] = Field(None, title="Published date")

    class Config:
        schema_extra = {
            "example": {
                "title": "Battle Brothers",
                "description": "Battle Brothers is a turn based tactical RPG which has"
                " you leading a mercenary company in a gritty, low-power, "
                "medieval fantasy world.",
                "published_date": date(2015, 4, 27),
            }
        }
