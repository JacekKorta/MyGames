from bson import ObjectId
from fastapi.testclient import TestClient
import pytest

from backend.main import app

client = TestClient(app)


class TestRoutes:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.fixture = {
            "title": "Battle Brothers",
            "description": "Battle Brothers is a turn based game.",
            "published_date": "2015-04-27",
        }
        client.post("/my-games/add-game", json=self.fixture)
        response = client.get("/my-games/get-games")
        self.game_id = response.json()[0].get("id")
        self.game_title = response.json()[0].get("title")
        self.game_desc = response.json()[0].get("description")
        self.game_published_date = response.json()[0].get("published_date")

    def test_get_games(self):
        response = client.get("/my-games/get-games")
        assert len(response.json()) == 1
        assert response.status_code == 200

    def test_get_game_data_success(self):
        response = client.get(f"/my-games/get-game/{self.game_id}")
        assert response.status_code == 200
        assert response.json().get("id") == self.game_id
        assert response.json().get("title") == self.game_title
        assert response.json().get("description") == self.game_desc
        assert response.json().get("published_date") == self.game_published_date

    def test_get_game_data_fail(self):
        fake_id = ObjectId()
        response = client.get(f"/my-games/get-game/{fake_id}")
        assert response.status_code == 404

    def test_update_game_data_success(self):
        payload = {
            "title": "Battle Brothers",
            "description": "Battle Brothers is a turn based RPG game.",
            "published_date": "2015-04-27",
        }
        client.put(f"/my-games/update-game/{self.game_id}", json=payload)
        response = client.get(f"/my-games/get-game/{self.game_id}")
        assert (
            response.json().get("description")
            == "Battle Brothers is a turn based RPG game."
        )
        assert response.status_code == 200

    def test_update_game_data_fail(self):
        fake_id = ObjectId()
        response = client.put(f"/my-games/update-game/{fake_id}")
        assert response.status_code == 422

    def test_delete_game_data_success(self):
        response = client.delete(f"/my-games/delete-game/{self.game_id}")
        response_2 = client.get(f"/my-games/get-game/{self.game_id}")
        assert response.status_code == 200
        assert response_2.status_code == 404

    def test_delete_game_data_fail(self):
        fake_id = ObjectId()
        response = client.delete(f"/my-games/delete-game/{fake_id}")
        assert response.status_code == 422
