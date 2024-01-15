from acas_auth.application.extensions import db


class PurchaseWTax(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    w_tax_code = db.Column(db.String(255))
    w_tax_name = db.Column(db.String(255))
    w_tax_rate = db.Column(db.Float())

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='purchase_w_taxes', lazy=True)

    def __str__(self):
        return self.w_tax_code
    
    def wt_rate(self):
        return self.w_tax_rate / 100
    