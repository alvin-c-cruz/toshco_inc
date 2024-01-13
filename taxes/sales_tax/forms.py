from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import SalesTax


@dataclass
class SalesTaxForm:
    id: int = None
    sales_tax_name: str = ""
    tax_rate: str = ""
    account_id: int = 0

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.sales_tax_name = object.sales_tax_name
        self.tax_rate = object.tax_rate
        self.account_id = object.account_id

    def save(self):
        if self.id is None:
            # Add a new record
            sales_tax = SalesTax(
                sales_tax_name=self.sales_tax_name,
                tax_rate=self.tax_rate,
                account_id=self.account_id
                )
            db.session.add(sales_tax)
        else:
            # Update an existing record
            sales_tax = SalesTax.query.get_or_404(self.id)
            if sales_tax:
                sales_tax.sales_tax_name = self.sales_tax_name
                sales_tax.tax_rate = self.tax_rate
                sales_tax.account_id = self.account_id
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('sales_tax_id')
        self.sales_tax_name = request_form.get('sales_tax_name')

        if type(request_form.get('tax_rate')) == str:
            value = request_form.get('tax_rate')
            if value.isnumeric() or (value.replace('.', '', 1).isdigit() and value.count('.') <= 1):
                self.tax_rate = float(value)
            else:
                self.tax_rate = 0
        else: 
            self.tax_rate = request_form.get('tax_rate')
    
        self.account_id = int(request_form.get('account_id'))

    def validate_on_submit(self):
        self.errors = {}
        # Sales Tax Name
        if not self.sales_tax_name:
            self.errors["sales_tax_name"] = "Please type sales tax name."
        else:
            existing_sales_tax = SalesTax.query.filter(func.lower(SalesTax.sales_tax_name) == func.lower(self.sales_tax_name), SalesTax.id != self.id).first()
            if existing_sales_tax:
                self.errors["sales_tax_name"] = "Sales Tax Name already exists. Please choose a different one."

        if not self.account_id:
            self.errors["account_id"] = "Please select account."

        if not self.errors:
            return True
        else:
            return False 
