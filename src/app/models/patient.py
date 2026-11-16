from src.app.extensions import db

class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    pesel = db.Column(db.String(32), nullable=False)
    facility_id = db.Column(
        db.Integer,
        db.ForeignKey("facility.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    analyses = db.relationship(
        "Analysis",
        back_populates="patient",
    )

    facility = db.relationship(
        "Facility",
        back_populates="patients",
    )