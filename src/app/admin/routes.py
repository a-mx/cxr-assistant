from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.app.admin import admin_bp
from src.app.admin.forms import RoleDecisionForm, FacilityForm
from src.app.extensions import db
from src.app.models import AuditLog, RoleRequest, AuditLog, Facility
from src.app.auth.permissions import can_manage_role_requests
from sqlalchemy.exc import IntegrityError

def _require_admin() -> None:
    if not can_manage_role_requests(current_user):
        abort(403)


@admin_bp.route("/role-requests")
@login_required
def role_requests():
    _require_admin()
    role_requests = RoleRequest.query.order_by(
        RoleRequest.status,
        RoleRequest.created_at.desc(),
    ).all()
    decision_form = RoleDecisionForm()
    return render_template(
        "admin/role_requests.html",
        role_requests=role_requests,
        decision_form=decision_form,
    )

@admin_bp.route("/facility/new", methods=["GET", "POST"])
@login_required
def add_facility():
    _require_admin()

    form = FacilityForm()

    if form.validate_on_submit():
        facility = Facility(
            name=form.name.data.strip(),
        )

        try:
            db.session.add(facility)
            db.session.flush()

            AuditLog.log(
                event_type="facility_created",
                user_id=current_user.id,
                description=f"Created facility {facility.id}",
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent", "")[:255],
            )

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append(
                "A facility with this name already exists."
            )
            return render_template(
                "admin/facility/new.html",
                form=form,
            )

        flash("Facility added successfully.", "success")
        return redirect(url_for("admin.facility_index"))

    return render_template(
        "admin/facility/new.html",
        form=form,
    )


@admin_bp.route("/facility")
@login_required
def facility_index():
    _require_admin()

    facilities = Facility.query.order_by(Facility.name).all()

    return render_template(
        "admin/facility/index.html",
        facilities=facilities,
    )


def _decide_role_request(role_request_id: int, status: str):
    _require_admin()
    role_request = db.session.get(RoleRequest, role_request_id)
    if role_request is None:
        abort(404)
    if role_request.status != "pending":
        flash("This request has already been reviewed.", "info")
        return redirect(url_for("admin.role_requests"))

    role_request.status = status
    role_request.reviewed_by_id = current_user.id
    role_request.reviewed_at = db.func.now()
    if status == "approved":
        role_request.user.role = role_request.requested_role
        role_request.user.facility_id = role_request.facility_id

    AuditLog.log(
        event_type=f"radiologist_role_request_{status}",
        user_id=current_user.id,
        description=(
            f"{status.title()} radiologist role request "
            f"for {role_request.user.username}"
        ),
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent", "")[:255],
    )
    db.session.commit()
    flash(
        f"Request for {role_request.user.username} was {status}.",
        "success",
    )
    return redirect(url_for("admin.role_requests"))


@admin_bp.route("/role-requests/<int:role_request_id>/approve", methods=["POST"])
@login_required
def approve_role_request(role_request_id: int):
    return _decide_role_request(role_request_id, "approved")


@admin_bp.route("/role-requests/<int:role_request_id>/reject", methods=["POST"])
@login_required
def reject_role_request(role_request_id: int):
    return _decide_role_request(role_request_id, "rejected")
