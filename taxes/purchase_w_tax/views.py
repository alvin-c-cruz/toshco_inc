from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import PurchaseWTax
from .forms import PurchaseWTaxForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    w_taxes = PurchaseWTax.query.order_by(PurchaseWTax.w_tax_name).all()

    context = {
        "w_taxes": w_taxes
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    if request.method == "POST":
        form = PurchaseWTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))
        else:
            flash("Error.", category="error")

    else:
        form = PurchaseWTaxForm()

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:w_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(w_tax_id):   
    if request.method == "POST":
        form = PurchaseWTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        w_tax = PurchaseWTax.query.get(w_tax_id)
        form = PurchaseWTaxForm()
        form.populate(w_tax)

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:w_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(w_tax_id):   
    w_tax = PurchaseWTax.query.get_or_404(w_tax_id)
    try:
        db.session.delete(w_tax)
        db.session.commit()
        flash(f"{w_tax} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {w_tax} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    w_taxes = [account for account in PurchaseWTax.query.order_by(PurchaseWTax.w_tax_name).all()]
    return Response(json.dumps(w_taxes), mimetype='application/json')