from datetime import datetime, timezone

from src.app.extensions import db


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    patient = db.relationship(
        "Patient",
        back_populates="analyses",
    )

    image_filename = db.Column(db.String(255), nullable=False)
    lateral_filename =  db.Column(db.String(255), nullable=True)

    stored_image_name = db.Column(db.String(255), nullable=False)
    stored_lateral_image_name = db.Column(db.String(255), nullable=True)

    user_prompt = db.Column(db.Text, nullable=True)

    generated_report = db.Column(db.Text, nullable=False)

    top_k = db.Column(db.Integer, nullable=False, default=5)
    retrieval_strategy = db.Column(
        db.String(50),
        nullable=False,
        default="image_only",
    )

    inference_time_ms = db.Column(db.Integer, nullable=True)

    retrieved_cases = db.Column(db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    revisions = db.relationship(
        "ReportRevision",
        back_populates="analysis",
        cascade="all, delete-orphan",
        order_by="ReportRevision.revision_number",
    )

    bounding_boxes = db.relationship(
        "BoundingBox",
        back_populates="analysis",
        cascade="all, delete-orphan",
    )

    @property
    def short_report(self) -> str:
        text = self.current_report.strip().replace("\n", " ")
        return text[:150] + "..." if len(text) > 150 else text

    @property
    def current_report(self) -> str:
        if self.revisions:
            return self.revisions[-1].content

        return self.generated_report

    @property
    def case_count(self) -> int:
        return len(self.retrieved_cases) if self.retrieved_cases else 0

    def __repr__(self) -> str:
        return (
            f"<Analysis id={self.id} user_id={self.user_id} "
            f"strategy={self.retrieval_strategy}>"
        )