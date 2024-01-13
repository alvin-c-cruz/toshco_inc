from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import PurchaseTax
from .forms import PurchaseTaxForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted
from ledger.account.models import Account

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    purchase_taxes = PurchaseTax.query.order_by(PurchaseTax.purchase_tax_name).all()

    context = {
        "purchase_taxes": purchase_taxes
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    account_dropdown = [{"id": account.id, "account": account} for account in Account.query.order_by('account_number').all()]
    if request.method == "POST":
        form = PurchaseTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))
        else:
            flash("Error.", category="error")

    else:
        form = PurchaseTaxForm()

    context = {
        "form": form,
        "account_dropdown": account_dropdown,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:purchase_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(purchase_tax_id):   
    account_dropdown = [{"id": account.id, "account": account} for account in Account.query.order_by('account_number').all()]
    if request.method == "POST":
        form = PurchaseTaxForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        purchase_tax = PurchaseTax.query.get(purchase_tax_id)
        form = PurchaseTaxForm()
        form.populate(purchase_tax)

    context = {
        "form": form,
        "account_dropdown": account_dropdown,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:purchase_tax_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(purchase_tax_id):   
    purchase_tax = PurchaseTax.query.get_or_404(purchase_tax_id)
    try:
        db.session.delete(purchase_tax)
        db.session.commit()
        flash(f"{purchase_tax} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {purchase_tax} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    purchase_taxes = [account for account in PurchaseTax.query.order_by(PurchaseTax.purchase_tax_name).all()]
    return Response(json.dumps(purchase_taxes), mimetype='application/json')