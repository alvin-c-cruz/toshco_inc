from acas_auth.application.extensions import db


class Vendor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vendor_name = db.Column(db.String(255))
    tin = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def __str__(self):
        return self.vendor_name
    