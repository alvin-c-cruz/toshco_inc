from acas_auth.application.extensions import db


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_name = db.Column(db.String(255))

    def __str__(self):
        return self.item_name
    