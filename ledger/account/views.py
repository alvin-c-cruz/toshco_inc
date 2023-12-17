from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
import json
from sqlalchemy.exc import IntegrityError
from .models import Account
from .forms import AccountForm
from acas_auth.application.extensions import db
from acas_auth.application.user import login_required, roles_accepted
from .. account_category import AccountCategory

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/")
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    accounts = Account.query.order_by(Account.account_number).all()

    context = {
        "accounts": accounts
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    account_category_dropdown = [{"id": category.id, "category_name": category.category_name} for category in AccountCategory.query.order_by('priority').all()]
    if request.method == "POST":
        form = AccountForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        form = AccountForm()

    context = {
        "form": form,
        "account_category_dropdown": account_category_dropdown
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:account_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(account_id):   
    account_category_dropdown = [{"id": category.id, "category_name": category.category_name} for category in AccountCategory.query.order_by('priority').all()]
    if request.method == "POST":
        form = AccountForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for(f'{app_name}.home'))

    else:
        account = Account.query.get(account_id)
        form = AccountForm()
        form.populate(account)

    context = {
        "form": form,
        "account_category_dropdown": account_category_dropdown
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:account_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(account_id):   
    account = Account.query.get_or_404(account_id)
    try:
        db.session.delete(account)
        db.session.commit()
        flash(f"{account} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {account} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/_autocomplete", methods=['GET'])
def autocomplete():
    accounts = [account for account in Account.query.order_by(Account.account_number).all()]
    return Response(json.dumps(accounts), mimetype='application/json')