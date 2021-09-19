from typing import Union

from fastapi import APIRouter, Body, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from backend.db.database import (
    add_game,
    delete_game,
    retrieve_game,
    retrieve_games,
    update_game,
)

from backend.models.game import (
    GameSchema,
    UpdateGameModel,
)

router = APIRouter()


@router.post("/add-game", response_description="Game data added into the database")
async def add_game_data(game: GameSchema = Body(...)) -> JSONResponse:
    game = jsonable_encoder(game)
    new_game = await add_game(game)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_game)


@router.get("/get-games", response_description="Games retrieved")
async def get_games() -> JSONResponse:
    games = await retrieve_games()
    return JSONResponse(status_code=status.HTTP_200_OK, content=games)


@router.get("/get-game/{id}", response_description="Game data retrieved")
async def get_game_data(id: str, response: Response) -> Union[JSONResponse, Response]:
    if game := await retrieve_game(id):
        return JSONResponse(status_code=status.HTTP_200_OK, content=game)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response


@router.put("/update-game/{id}", response_description="Game data updated")
async def update_game_data(
        id: str, response: Response, request_data: UpdateGameModel = Body(...)
) -> Response:
    request_data = {k: v for k, v in request_data.dict().items() if v is not None}
    if await update_game(id, request_data):
        response.status_code = status.HTTP_200_OK
        return response
    response.status_code = status.HTTP_404_NOT_FOUND
    return response


@router.delete("/delete-game/{id}", response_description="Game data deleted from the database")
async def delete_game_data(id: str, response: Response) -> Union[JSONResponse, Response]:
    if await delete_game(id):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": f"Game with ID: {id} was removed"},
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    return response
