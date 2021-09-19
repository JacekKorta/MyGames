from datetime import datetime, date
from typing import List, Optional, Union

from bson.objectid import ObjectId
import motor.motor_asyncio

from backend.db.db_config import path

client = motor.motor_asyncio.AsyncIOMotorClient(path)
database = client.games
games_collection = database.get_collection("games_collection")


def datetime_to_date(published_date: Union[datetime, date]) -> Union[str, date]:
    if isinstance(published_date, datetime):
        return published_date.strftime("%Y-%m-%d")
    return published_date


def date_to_datetime(published_date: date):
    return datetime.combine(published_date, datetime.min.time())


def game_helper(game) -> dict:
    return {
        "id": str(game["_id"]),
        "title": game["title"],
        "description": game["description"],
        "published_date": datetime_to_date(game["published_date"]),
    }


async def retrieve_games() -> List:
    games = []
    async for game in games_collection.find():
        games.append(game_helper(game))
    return games


async def add_game(game_data: dict) -> dict:
    game = await games_collection.insert_one(game_data)
    new_game = await games_collection.find_one({"_id": game.inserted_id})
    return game_helper(new_game)


async def retrieve_game(id: str) -> Optional[dict]:
    if game := await games_collection.find_one({"_id": ObjectId(id)}):
        return game_helper(game)


async def update_game(id: str, data: dict) -> Optional[bool]:
    if len(data) < 1:
        return False
    data["published_date"] = date_to_datetime(data["published_date"])
    if await games_collection.find_one({"_id": ObjectId(id)}):
        updated_game = await games_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_game:
            return True
        return False


async def delete_game(id: str) -> Optional[bool]:
    if await games_collection.find_one({"_id": ObjectId(id)}):
        await games_collection.delete_one({"_id": ObjectId(id)})
        return True
