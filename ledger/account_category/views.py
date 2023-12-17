from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import AccountCategory
from .forms import AccountCategoryForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    account_categories = AccountCategory.query.order_by(AccountCategory.priority).all()

    context = {
        "account_categories": account_categories
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    if request.method == "POST":
        form = AccountCategoryForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        form = AccountCategoryForm()

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:account_category_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(account_category_id):   
    if request.method == "POST":
        form = AccountCategoryForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        account_category = AccountCategory.query.get(account_category_id)
        form = AccountCategoryForm()
        form.populate(account_category)

    context = {
        "form": form,
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:account_category_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(account_category_id):   
    account_category = AccountCategory.query.get_or_404(account_category_id)
    try:
        db.session.delete(account_category)
        db.session.commit()
        flash(f"{account_category} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {account_category} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    account_categories = [category for category in AccountCategory.query.order_by(AccountCategory.priority).all()]
    return Response(json.dumps(account_categories), mimetype='application/json')