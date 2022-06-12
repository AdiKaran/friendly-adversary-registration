from .db import db
from sqlalchemy.dialects.postgresql import JSON


class Adversary(db.Model):
    __tablename__ = "adversary"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    planned_activity = db.Column(JSON,nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ip_address": self.ip_address,
            "email" : self.email,
            "planned_activity_json": self.planned_activity
        }
