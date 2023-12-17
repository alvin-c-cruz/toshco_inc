from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import AccountCategory


@dataclass
class AccountCategoryForm:
    id: int = None
    category_name: str = ""
    priority: str = ""

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.category_name = object.category_name
        self.priority = object.priority

    def save(self):
        if self.id is None:
            # Add a new record
            account_category = AccountCategory(
                category_name=self.category_name, 
                priority=self.priority
                )
            db.session.add(account_category)
        else:
            # Update an existing record
            account_category = AccountCategory.query.get_or_404(self.id)
            if account_category:
                account_category.category_name = self.category_name
                account_category.priority = self.priority
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('account_category_id')
        self.category_name = request_form.get('category_name')
        self.priority = request_form.get('priority')

    def validate_on_submit(self):
        self.errors = {}
        # Category Name
        if not self.category_name:
            self.errors["category_name"] = "Please type category."
        else:
            existing_category = AccountCategory.query.filter(func.lower(AccountCategory.category_name) == func.lower(self.category_name), AccountCategory.id != self.id).first()
            if existing_category:
                self.errors["category_name"] = "Category already exists. Please choose a different one."

        # Priority
        if not self.priority:
            self.errors["priority"] = "Please type priority."

        if not self.errors:
            return True
        else:
            return False    
