from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import PurchaseTax


@dataclass
class PurchaseTaxForm:
    id: int = None
    purchase_tax_name: str = ""
    account_id: int = 0

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.purchase_tax_name = object.purchase_tax_name
        self.account_id = object.account_id

    def save(self):
        if self.id is None:
            # Add a new record
            purchase_tax = PurchaseTax(
                purchase_tax_name=self.purchase_tax_name,
                account_id=self.account_id
                )
            db.session.add(purchase_tax)
        else:
            # Update an existing record
            purchase_tax = PurchaseTax.query.get_or_404(self.id)
            if purchase_tax:
                purchase_tax.purchase_tax_name = self.purchase_tax_name
                purchase_tax.account_id = self.account_id
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('purchase_tax_id')
        self.purchase_tax_name = request_form.get('purchase_tax_name')
        self.account_id = int(request_form.get('account_id'))

    def validate_on_submit(self):
        self.errors = {}
        # Purchase Tax Name
        if not self.purchase_tax_name:
            self.errors["purchase_tax_name"] = "Please type purchase tax name."
        else:
            existing_ = PurchaseTax.query.filter(func.lower(PurchaseTax.purchase_tax_name) == func.lower(self.purchase_tax_name), PurchaseTax.id != self.id).first()
            if existing_:
                self.errors["purchase_tax_name"] = "Purchase Tax Name already exists. Please choose a different one."

        if not self.account_id:
            self.errors["account_id"] = "Please select account."

        if not self.errors:
            return True
        else:
            return False 
