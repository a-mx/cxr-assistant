from flask import Blueprint

analyze_bp = Blueprint(
    "analyze",
    __name__,
    url_prefix="/analyze",
    template_folder="templates",
)