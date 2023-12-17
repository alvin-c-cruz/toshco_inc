from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import Measure
from .forms import MeasureForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    measures = Measure.query.order_by(Measure.measure_name).all()

    context = {
        "measures": measures
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    if request.method == "POST":
        form = MeasureForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))
    else:
        form = MeasureForm()

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:measure_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(measure_id):   
    if request.method == "POST":
        form = MeasureForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        measure = Measure.query.get(measure_id)
        form = MeasureForm()
        form.populate(measure)

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:measure_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(measure_id):   
    measure = Measure.query.get_or_404(measure_id)
    try:
        db.session.delete(measure)
        db.session.commit()
        flash(f"{measure} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {measure} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    measures = [measure for measure in Measure.query.order_by(Measure.measure_name).all()]
    return Response(json.dumps(measures), mimetype='application/json')
