from datetime import datetime, timezone

from src.app.extensions import db


class RoleRequest(db.Model):
    __tablename__ = "role_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requested_role = db.Column(db.String(20), nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref("role_requests", lazy="dynamic"),
    )
    reviewed_by = db.relationship(
        "User",
        foreign_keys=[reviewed_by_id],
    )

    def __repr__(self) -> str:
        return (
            f"<RoleRequest user_id={self.user_id} "
            f"role={self.requested_role} status={self.status}>"
        )
