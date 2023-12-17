from flask import Blueprint, render_template
from acas_auth.application.user import login_required


bp = Blueprint('main', __name__, template_folder="pages")


@bp.route("/")
@login_required
def home():
    return render_template("main/home.html")
