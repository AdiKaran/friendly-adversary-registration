import json
from database.models import Adversary


def test_register_adversary(client, session):
    url = "/api/adversary"
    request_body = {"ip_address": "168.212. 226.204", "name": "adversary name"}
    response = client.post(url, json=request_body)
    assert response.status_code == 200
    response_object = json.loads((response.get_data()))

    assert response_object["ip_address"] == "168.212. 226.204"
    assert response_object["name"] == "adversary name"
    assert response_object["email"] is None
    assert response_object["planned_activity_json"] is None

    request_body = {
        "ip_address": "168.212. 226.204",
        "name": "adversary name",
        "planned_activity_json": {"activity": "some activity"},
        "email": "baz@spam.foo",
    }
    response = client.post(url, json=request_body)
    response_object = json.loads((response.get_data()))

    assert response_object["ip_address"] == "168.212. 226.204"
    assert response_object["name"] == "adversary name"
    assert response_object["email"] == "baz@spam.foo"
    assert response_object["planned_activity_json"] == {"activity": "some activity"}


def test_list_empty_adversaries(client, session):
    url = "/api/adversary"
    response = client.get(url)
    assert response.status_code == 200
    response_object = json.loads((response.get_data()))

    assert response_object["adversaries"] == []


def test_list_adversaries(client, session):
    url = "/api/adversary"

    adversary1 = Adversary(
        name="foo",
        ip_address="168.212. 226.204",
        email="spam@spam.com",
        planned_activity={
            "timestamp": "1973-08-12T02:13:03+0000",
            "activity": "some other activity",
        },
    )

    adversary2 = Adversary(
        name="bar",
        ip_address="168.212. 226.207",
        email="baz@spam.foo",
        planned_activity={"activity": "some activity"},
    )

    session.add(adversary1)
    session.add(adversary2)
    session.commit()

    response = client.get(url)
    assert response.status_code == 200
    response_object = json.loads((response.get_data()))

    assert {
        "email": "baz@spam.foo",
        "id": 2,
        "ip_address": "168.212. 226.207",
        "name": "bar",
        "planned_activity_json": {"activity": "some activity"},
    } in response_object["adversaries"]
    assert {
        "email": "spam@spam.com",
        "id": 1,
        "ip_address": "168.212. 226.204",
        "name": "foo",
        "planned_activity_json": {
            "activity": "some other activity",
            "timestamp": "1973-08-12T02:13:03+0000",
        },
    } in response_object["adversaries"]


def test_get_nonexistent_adversary(client, session):
    url = "/api/adversary/42"
    response = client.get(url)
    assert response.status_code == 404


def test_get_adversary(client, session):
    adversary = Adversary(
        name="adversary_name",
        ip_address="168.212. 226.204",
        email="email@website.domain",
        planned_activity={"foo": "bar", "bar": "baz"},
    )
    session.add(adversary)
    session.commit()

    url = f"/api/adversary/{adversary.id}"
    response = client.get(url)
    assert response.status_code == 200
    response_object = json.loads((response.get_data()))

    assert "id" in response_object and response_object["id"] == adversary.id
    assert (
        "email" in response_object
        and response_object["email"] == "email@website.domain"
    )
    assert "name" in response_object and response_object["name"] == "adversary_name"
    assert (
        "ip_address" in response_object
        and response_object["ip_address"] == "168.212. 226.204"
    )
    assert "planned_activity_json" in response_object and response_object[
        "planned_activity_json"
    ] == {"foo": "bar", "bar": "baz"}


def test_delete_nonexistent_adversary(client, session):
    url = "/api/adversary/42"
    response = client.delete(url)
    assert response.status_code == 404


def test_delete_adversary(client, session):
    adversary = Adversary(
        name="adversary_name",
        ip_address="168.212. 226.204",
        email="email@website.domain",
        planned_activity={"foo": "bar", "bar": "baz"},
    )
    session.add(adversary)
    session.commit()

    url = f"/api/adversary/{adversary.id}"
    response = client.delete(url)
    assert response.status_code == 200

    retrieved_adversary = Adversary.query.get(adversary.id)
    assert retrieved_adversary is None


def test_patch_nonexistent_adversary(client, session):
    url = "/api/adversary/42"
    response = client.patch(
        url, json={"ip_address": "168.212. 226.204", "name": "adversary name"}
    )
    assert response.status_code == 404


def test_update_adversary(client, session):
    adversary = Adversary(
        name="adversary_name",
        ip_address="168.212. 226.204",
        email="email@website.domain",
        planned_activity={},
    )
    session.add(adversary)
    session.commit()

    request_body = {
        "ip_address": "424.242. 424.242",
        "name": "new name",
        "planned_activity_json": {"activity": "some activity"},
        "email": "newemail@spam.foo",
    }
    adversary_id = adversary.id
    url = f"/api/adversary/{adversary_id}"
    response = client.patch(url, json=request_body)
    assert response.status_code == 200

    adversary = Adversary.query.get(adversary_id)

    assert adversary.id == adversary_id
    assert adversary.email == "newemail@spam.foo"
    assert adversary.planned_activity == {"activity": "some activity"}
    assert adversary.ip_address == "424.242. 424.242"
