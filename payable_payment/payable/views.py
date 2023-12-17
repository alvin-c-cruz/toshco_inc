from flask import Blueprint, render_template, request, redirect, url_for, flash
import datetime
from sqlalchemy.exc import IntegrityError
from .models import Payable, PayableDetail
from .forms import Form
from .. item import Item
from .. measure import Measure
from ... ledger.account import Account
from .. vendor import Vendor
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted
from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    payables = Payable.query.order_by(
        Payable.record_date.desc(), Payable.id.desc()).all()

    context = {
        "payables": payables
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    item_dropdown = [{"id": item.id, "item_name": item.item_name} for item in Item.query.order_by('item_name').all()]
    measure_dropdown = [{"id": measure.id, "measure_name": measure.measure_name} for measure in Measure.query.order_by('measure_name').all()]
    vendor_dropdown = [{"id": vendor.id, "vendor_name": vendor.vendor_name} for vendor in Vendor.query.order_by('vendor_name').all()]
    account_dropdown = [{"id": account.id, "account": account} for account in Account.query.order_by('account_number').all()]
    if request.method == "POST":
        form = Form()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            flash(f"{form.ap_number} has been added.", category="success")
            return redirect(url_for(f'{app_name}.home'))

    else:
        form = Form()
        form.record_date = str(datetime.date.today())[:10]


    context = {
        "form": form,
        "item_dropdown": item_dropdown,
        "measure_dropdown": measure_dropdown,
        "vendor_dropdown": vendor_dropdown,
        "account_dropdown": account_dropdown,        
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/edit/<int:payable_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(payable_id):   
    item_dropdown = [{"id": item.id, "item_name": item.item_name} for item in Item.query.order_by('item_name').all()]
    measure_dropdown = [{"id": measure.id, "measure_name": measure.measure_name} for measure in Measure.query.order_by('measure_name').all()]
    vendor_dropdown = [{"id": vendor.id, "vendor_name": vendor.vendor_name} for vendor in Vendor.query.order_by('vendor_name').all()]
    account_dropdown = [{"id": account.id, "account": account} for account in Account.query.order_by('account_number').all()]

    if request.method == "POST":
        form = Form()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            flash(f"{form.ap_number} has been updated.", category="success")
            return redirect(url_for(f'{app_name}.edit', payable_id=payable_id))

    else:
        payable = Payable.query.get(payable_id)
        form = Form(
            id=payable.id,
            ap_number=payable.ap_number,
            record_date=payable.record_date,
            vendor_id=payable.vendor_id,
            invoice_number=payable.invoice_number,
        )

        for i, detail in enumerate(payable.payable_details):
            form.details[i][1].id = detail.id
            form.details[i][1].quantity = detail.quantity
            form.details[i][1].unit_price = detail.unit_price
            form.details[i][1].measure_id = detail.measure_id
            form.details[i][1].item_id = detail.item_id
            form.details[i][1].account_id = detail.account_id

    context = {
        "form": form,
        "item_dropdown": item_dropdown,
        "measure_dropdown": measure_dropdown,
        "vendor_dropdown": vendor_dropdown,
        "account_dropdown": account_dropdown,        
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:payable_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(payable_id):   
    payable = Payable.query.get(payable_id)
    details = PayableDetail.query.filter(PayableDetail.payable_id==payable_id).all()
    try:
        for detail in details:
            db.session.delete(detail)
        db.session.delete(payable)
        db.session.commit()
        flash(f"{payable.ap_number} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {payable} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))
