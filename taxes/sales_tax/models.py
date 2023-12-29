from acas_auth.application.extensions import db


class SalesTax(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sales_tax_name = db.Column(db.String(255))

    def __str__(self):
        return self.sales_tax_name
    