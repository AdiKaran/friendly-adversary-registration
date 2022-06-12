from flask import make_response
from database.db import db
from database.models import Adversary
from werkzeug.exceptions import NotFound


def register_adversary(body):
    adversary = Adversary(
        name=body["name"],
        ip_address=body["ip_address"],
        email=body["email"],
        planned_activity=body["planned_activity_json"],
    )
    if "email" in body:
        adversary.email = body["email"]
    if "planned_activity " in body:
        adversary.planned_activity = body["planned_activity_json"]

    db.session.add(adversary)
    db.session.commit()
    return adversary.to_dict()


def list_adversaries(page, pageSize):
    query_results = (
        db.session.query(Adversary)
        .group_by(Adversary.id)
        .order_by(Adversary.id.desc())
        .paginate(page, pageSize)
    )

    adversaries = []
    for row in query_results.items:
        adversaries.append(row.to_dict())

    return {
        "adversaries": adversaries,
        "pageInfo": {
            "page": page,
            "pageSize": pageSize,
            "totalResults": query_results.total,
        },
    }


def get_adversary(id):
    adversary = Adversary.query.get(id)
    if not adversary:
        raise NotFound(f"adversary with id {id} not found")
    return adversary.to_dict()


def delete_adversary(id):
    adversary = Adversary.query.get(id)
    if not adversary:
        raise NotFound(f"adversary with id {id} not found")

    db.session.delete(adversary)
    db.session.commit()
    return make_response(f"Successfully deleted adversary with id {id}", 200)


def update_adversary(id, body):
    adversary = Adversary.query.get(id)
    if not adversary:
        raise NotFound(f"adversary with id {id} not found")

    adversary.name = body["name"]
    adversary.ip_address = body["ip_address"]
    adversary.email = body["email"]
    adversary.planned_activity = body["planned_activity_json"]

    db.session.add(adversary)
    db.session.commit()
    return make_response(f"Successfully updated adversary with id {id}", 200)
