from acas_auth.application.extensions import db


class PurchaseTax(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    purchase_tax_name = db.Column(db.String(255))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='purchase_taxes', lazy=True)

    def __str__(self):
        return self.purchase_tax_name
