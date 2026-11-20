import json
from pathlib import Path

import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_flow_list_success(client):
    response = client.post(
        "/api/jobs/flow_def/list",
        json={
            "page_num": 1,
            "page_size": 2
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["code"] == 1
    assert data["data"]["total"] == 3
    assert len(data["data"]["list"]) == 2


def test_flow_list_invalid_page(client):
    response = client.post(
        "/api/jobs/flow_def/list",
        json={
            "page_num": -1,
            "page_size": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["code"] == 0

    samples_path = (
            Path(__file__).resolve().parent.parent
            / "evaluations"
            / "samples.json"
    )

    with open(samples_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    @pytest.mark.parametrize(
        "case",
        test_cases,
        ids=[case["name"] for case in test_cases]
    )
    def test_flow_list_data_driven(client, case):
        response = client.post(
            "/api/jobs/flow_def/list",
            json=case["input"]
        )

        assert response.status_code == case["expected_status"]

        data = response.get_json()

        assert data["code"] == case["expected_code"]

        if "expected_count" in case:
            assert len(data["data"]["list"]) == case["expected_count"]



samples_path = (
    Path(__file__).resolve().parent.parent
    / "evaluations"
    / "samples.json"
)

with open(samples_path, "r", encoding="utf-8") as f:
    test_cases = json.load(f)


@pytest.mark.parametrize(
    "case",
    test_cases,
    ids=[case["name"] for case in test_cases]
)
def test_flow_list_data_driven(client, case):

    response = client.post(
        "/api/jobs/flow_def/list",
        json=case["input"]
    )

    assert response.status_code == case["expected_status"]

    data = response.get_json()

    assert data["code"] == case["expected_code"]

    if "expected_count" in case:
        assert len(data["data"]["list"]) == case["expected_count"]