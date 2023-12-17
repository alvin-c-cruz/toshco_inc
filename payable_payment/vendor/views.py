from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import Vendor
from .forms import VendorForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    vendors = Vendor.query.order_by(Vendor.vendor_name).all()

    context = {
        "vendors": vendors
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    if request.method == "POST":
        form = VendorForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        form = VendorForm()

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:vendor_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(vendor_id):   
    if request.method == "POST":
        form = VendorForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        vendor = Vendor.query.get(vendor_id)
        form = VendorForm()
        form.populate(vendor)

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:vendor_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(vendor_id):   
    vendor = Vendor.query.get_or_404(vendor_id)
    try:
        db.session.delete(vendor)
        db.session.commit()
        flash(f"{vendor} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {vendor} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    vendors = [vendor for vendor in Vendor.query.order_by(Vendor.vendor_name).all()]
    return Response(json.dumps(vendors), mimetype='application/json')