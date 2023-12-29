from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import SalesTax


@dataclass
class SalesTaxForm:
    id: int = None
    sales_tax_name: str = ""

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.sales_tax_name = object.sales_tax_name

    def save(self):
        if self.id is None:
            # Add a new record
            sales_tax = SalesTax(
                sales_tax_name=self.sales_tax_name
                )
            db.session.add(sales_tax)
        else:
            # Update an existing record
            sales_tax = SalesTax.query.get_or_404(self.id)
            if sales_tax:
                sales_tax.sales_tax_name = self.sales_tax_name
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('sales_tax_id')
        self.sales_tax_name = request_form.get('sales_tax_name')

    def validate_on_submit(self):
        self.errors = {}
        # Sales Tax Name
        if not self.sales_tax_name:
            self.errors["sales_tax_name"] = "Please type sales tax name."
        else:
            existing_sales_tax = SalesTax.query.filter(func.lower(SalesTax.sales_tax_name) == func.lower(self.sales_tax_name), SalesTax.id != self.id).first()
            if existing_sales_tax:
                self.errors["sales_tax_name"] = "Sales Tax Name already exists. Please choose a different one."

        if not self.errors:
            return True
        else:
            return False 
