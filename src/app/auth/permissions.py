from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(role: str):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def can_manage_role_requests(user) -> bool:
    return user.is_authenticated and user.role == "admin"


def can_manage_patients(user) -> bool:
    return user.is_authenticated and user.role == "radiologist"


def can_access_facility(user, facility_id: int | None) -> bool:
    return (
        can_manage_patients(user)
        and facility_id is not None
        and user.facility_id == facility_id
    )


def can_access_patient(user, patient) -> bool:
    return can_access_facility(user, patient.facility_id)


def can_access_analysis(user, analysis) -> bool:
    return can_access_patient(user, analysis.patient)
