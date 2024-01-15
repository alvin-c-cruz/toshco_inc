from dataclasses import dataclass
from sqlalchemy import func
import re
from acas_auth.application.extensions import db
from .models import PurchaseWTax


@dataclass
class PurchaseWTaxForm:
    id: int = None
    w_tax_code: str = ""
    w_tax_name: str = ""
    w_tax_rate: str = ""
    account_id: int = 0

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.w_tax_code = object.w_tax_code
        self.w_tax_name = object.w_tax_name
        self.w_tax_rate = object.w_tax_rate
        self.account_id = object.account_id

    def save(self):
        if self.id is None:
            # Add a new record
            w_tax = PurchaseWTax(
                w_tax_code=self.w_tax_code,
                w_tax_name=self.w_tax_name,
                w_tax_rate=self.w_tax_rate,
                account_id=self.account_id
                )
            db.session.add(w_tax)
        else:
            # Update an existing record
            w_tax = PurchaseWTax.query.get_or_404(self.id)
            if w_tax:
                w_tax.w_tax_code = self.w_tax_code
                w_tax.w_tax_name = self.w_tax_name
                w_tax.w_tax_rate = self.w_tax_rate
                w_tax.account_id = self.account_id
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('w_tax_id')
        self.w_tax_code = request_form.get('w_tax_code')
        self.w_tax_name = request_form.get('w_tax_name')
        self.w_tax_rate = request_form.get('w_tax_rate')
        self.account_id = request_form.get('account_id')

    def validate_on_submit(self):
        self.errors = {}
        # W Tax Code
        if not self.w_tax_code:
            self.errors["w_tax_code"] = "Please type ATC."
        else:
            existing_w_tax = PurchaseWTax.query.filter(func.lower(PurchaseWTax.w_tax_code) == func.lower(self.w_tax_code), PurchaseWTax.id != self.id).first()
            if existing_w_tax:
                self.errors["w_tax_code"] = "ATC already exists. Please choose a different one."

        # W Tax Name
        if not self.w_tax_name:
            self.errors["w_tax_name"] = "Please type withholding tax description."
        else:
            existing_w_tax = PurchaseWTax.query.filter(func.lower(PurchaseWTax.w_tax_name) == func.lower(self.w_tax_name), PurchaseWTax.id != self.id).first()
            if existing_w_tax:
                self.errors["w_tax_name"] = "Description already exists. Please choose a different one."

        # W Tax Rate
        if not self.w_tax_rate:
            self.errors["w_tax_rate"] = "Please type applicable tax."
        else:
            if not check_format(self.w_tax_rate):
                self.errors["w_tax_rate"] = "Please follow 0.00 format. (ei. 2.00)"
        
        # Account Title
        if not self.account_id:
            self.errors["account_id"] = "Please select account title."

        if not self.errors:
            return True
        else:
            return False 


def check_format(input_str):
    pattern = r'^\d{1,3}\.\d{2}$'
    return bool(re.match(pattern, input_str))