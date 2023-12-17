from acas_auth.application.extensions import db


class Measure(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    measure_name = db.Column(db.String(255))
    symbol = db.Column(db.String(255))

    def __str__(self):
        return self.symbol
    