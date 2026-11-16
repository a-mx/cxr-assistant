from src.app.extensions import db

class Facility(db.Model):
    __tablename__ = "facility"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    users = db.relationship(
        "User",
        back_populates="facility",
    )
    patients = db.relationship(
        "Patient",
        back_populates="facility",
    )