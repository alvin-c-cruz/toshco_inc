from acas_auth.application.extensions import db


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_number = db.Column(db.String(255))
    account_title = db.Column(db.String(255))
    
    account_category_id = db.Column(db.Integer, db.ForeignKey("account_category.id"), nullable=False)
    account_category = db.relationship('AccountCategory', backref='accounts', lazy=True)

    def __str__(self):
        return f"{self.account_number}: {self.account_title}"
    