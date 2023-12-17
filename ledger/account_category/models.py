from acas_auth.application.extensions import db


class AccountCategory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(255))
    priority = db.Column(db.String(255))

    def __str__(self):
        return self.category_name
    