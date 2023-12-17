from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import Item


@dataclass
class ItemForm:
    id: int = None
    item_name: str = ""

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.item_name = object.item_name

    def save(self):
        if self.id is None:
            # Add a new record
            item = Item(
                item_name=self.item_name
                )
            db.session.add(item)
        else:
            # Update an existing record
            item = Item.query.get_or_404(self.id)
            if item:
                item.item_name = self.item_name
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('item_id')
        self.item_name = request_form.get('item_name')

    def validate_on_submit(self):
        self.errors = {}
        # Item Name
        if not self.item_name:
            self.errors["item_name"] = "Please type item name."
        else:
            existing_item = Item.query.filter(func.lower(Item.item_name) == func.lower(self.item_name), Item.id != self.id).first()
            if existing_item:
                self.errors["item_name"] = "Item already exists."

        if not self.errors:
            return True
        else:
            return False    
