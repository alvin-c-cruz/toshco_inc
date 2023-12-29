from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import SalesTax
from .forms import SalesTaxForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    sales_taxes = SalesTax.query.order_by(SalesTax.sales_tax_name).all()

    context = {
        "sales_taxes": sales_taxes
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    if request.method == "POST":
        form = SalesTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))
        else:
            flash("Error.", category="error")

    else:
        form = SalesTaxForm()

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:sales_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(sales_tax_id):   
    if request.method == "POST":
        form = SalesTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        sales_tax = SalesTax.query.get(sales_tax_id)
        form = SalesTaxForm()
        form.populate(sales_tax)

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:sales_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(sales_tax_id):   
    sales_tax = SalesTax.query.get_or_404(sales_tax_id)
    try:
        db.session.delete(sales_tax)
        db.session.commit()
        flash(f"{sales_tax} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {sales_tax} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    sales_taxes = [account for account in SalesTax.query.order_by(SalesTax.sales_tax_name).all()]
    return Response(json.dumps(sales_taxes), mimetype='application/json')