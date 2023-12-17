from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import Measure


@dataclass
class MeasureForm:
    id: int = None
    measure_name: str = ""
    symbol: str = ""

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.measure_name = object.measure_name
        self.symbol = object.symbol

    def save(self):
        if self.id is None:
            # Add a new record
            measure = Measure(
                measure_name=self.measure_name,
                symbol=self.symbol
                )
            db.session.add(measure)
        else:
            # Update an existing record
            measure = Measure.query.get_or_404(self.id)
            if measure:
                measure.measure_name = self.measure_name
                measure.symbol = self.symbol
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('measure_id')
        self.measure_name = request_form.get('measure_name')
        self.symbol = request_form.get('symbol')

    def validate_on_submit(self):
        self.errors = {}
        # Measure Name
        if not self.measure_name:
            self.errors["measure_name"] = "Please type measure name."
        else:
            existing_measure = Measure.query.filter(func.lower(Measure.measure_name) == func.lower(self.measure_name), Measure.id != self.id).first()
            if existing_measure:
                self.errors["measure_name"] = "Measure already exists."

        # Symbol
        if not self.symbol:
            self.errors["symbol"] = "Please type symbol."
        else:
            existing_measure = Measure.query.filter(func.lower(Measure.symbol) == func.lower(self.symbol), Measure.id != self.id).first()
            if existing_measure:
                self.errors["Symbol"] = "Symbol already used."

        if not self.errors:
            return True
        else:
            return False    
