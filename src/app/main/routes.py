from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    request,
    url_for,
)
from flask_login import current_user, login_required

from src.app.extensions import db
from src.app.main.forms import RadiologistRequestForm
from src.app.models import AuditLog, RoleRequest, Facility
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html')


@main_bp.route("/request-radiologist", methods=["GET", "POST"])
@login_required
def request_radiologist():
    if current_user.role != "user":
        flash("Only users with the standard role can request radiologist access.", "warning")
        return redirect(url_for("main.index"))

    pending_request = RoleRequest.query.filter_by(
        user_id=current_user.id,
        requested_role="radiologist",
        status="pending",
    ).first()

    form = RadiologistRequestForm()

    form.facility_id.choices = [
        (facility.id, facility.name)
        for facility in Facility.query.order_by(Facility.name).all()
    ]

    if form.validate_on_submit():
        if pending_request:
            flash("You already have a pending radiologist role request.", "info")
        else:
            db.session.add(RoleRequest(
                user_id=current_user.id,
                requested_role="radiologist",
                facility_id=form.facility_id.data,
            ))

            AuditLog.log(
                event_type="radiologist_role_requested",
                user_id=current_user.id,
                description=f"Radiologist role requested by {current_user.username}",
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent", "")[:255],
            )
            db.session.commit()
            flash("Your request has been submitted for review.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "main/request_radiologist.html",
        form=form,
        pending_request=pending_request,
    )