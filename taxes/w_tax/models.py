from acas_auth.application.extensions import db


class WTax(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    w_tax_code = db.Column(db.String(255))
    w_tax_name = db.Column(db.String(255))
    w_tax_rate = db.Column(db.String(255))

    def __str__(self):
        return self.w_tax_code
    