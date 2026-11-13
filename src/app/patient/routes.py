from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    request,
)
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from src.app.patient import patient_bp
from src.app.patient.forms import PatientForm
from src.app.extensions import db
from src.app.models import Patient, AuditLog


def _can_manage_patients() -> bool:
    return current_user.role in {"admin", "user"}


@patient_bp.route("/")
@login_required
def index():
    if not _can_manage_patients():
        abort(403)

    patients = Patient.query.order_by(
        Patient.surname,
        Patient.name,
    ).all()

    return render_template(
        "patient/index.html",
        patients=patients,
    )


@patient_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if not _can_manage_patients():
        abort(403)

    form = PatientForm()

    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data.strip(),
            surname=form.surname.data.strip(),
            pesel=form.pesel.data.strip(),
        )

        try:
            db.session.add(patient)
            db.session.flush()

            AuditLog.log(
                event_type="patient_created",
                user_id=current_user.id,
                description=f"Created patient record {patient.id}",
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent", "")[:255],
            )

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.pesel.errors.append(
                "A patient with this PESEL already exists."
            )
            return render_template(
                "patient/new.html",
                form=form,
            )

        flash("Patient added successfully.", "success")
        return redirect(url_for("patient.index"))

    return render_template(
        "patient/new.html",
        form=form,
    )