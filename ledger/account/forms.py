from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import Account


@dataclass
class AccountForm:
    id: int = None
    account_number: str = ""
    account_title: str = ""
    account_category_id: int = None

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.account_number = object.account_number
        self.account_title = object.account_title
        self.account_category_id = object.account_category_id

    def save(self):
        if self.id is None:
            # Add a new record
            account = Account(
                account_number=self.account_number, 
                account_title=self.account_title, 
                account_category_id=self.account_category_id
                )
            db.session.add(account)
        else:
            # Update an existing record
            account = Account.query.get_or_404(self.id)
            if account:
                account.account_number = self.account_number
                account.account_title = self.account_title
                account.account_category_id = self.account_category_id
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('account_id')
        self.account_number = request_form.get('account_number')
        self.account_title = request_form.get('account_title')
        self.account_category_id = int(request_form.get('account_category_id'))

    def validate_on_submit(self):
        self.errors = {}
        # Account Number
        if not self.account_number:
            self.errors["account_number"] = "Please type account number."
        else:
            existing_account = Account.query.filter(func.lower(Account.account_number) == func.lower(self.account_number), Account.id != self.id).first()
            if existing_account:
                self.errors["account_number"] = "Account Number already exists. Please choose a different one."

        # Account Title
        if not self.account_title:
            self.errors["account_title"] = "Please type account title."
        else:
            existing_account = Account.query.filter(func.lower(Account.account_title) == func.lower(self.account_title), Account.id != self.id).first()
            if existing_account:
                self.errors["account_title"] = "Account Title already exists. Please choose a different one."

        # Account Category
        if not self.account_category_id:
            self.errors["account_category_id"] = "Please select category."

        if not self.errors:
            return True
        else:
            return False    
