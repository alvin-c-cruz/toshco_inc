from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import Vendor


@dataclass
class VendorForm:
    id: int = None
    vendor_name: str = ""
    tin: str = ""
    address: str = ""

    errors = {}

    def populate(self, object):
        self.id = object.id
        self.vendor_name = object.vendor_name
        self.tin = object.tin
        self.address = object.address

    def save(self):
        if self.id is None:
            # Add a new record
            vendor = Vendor(
                vendor_name=self.vendor_name, 
                tin=self.tin, 
                address=self.address
                )
            db.session.add(vendor)
        else:
            # Update an existing record
            vendor = Vendor.query.get_or_404(self.id)
            if vendor:
                vendor.vendor_name = self.vendor_name
                vendor.tin = self.tin
                vendor.address = self.address
        db.session.commit()

    def post(self, request_form):
        self.id = request_form.get('vendor_id')
        self.vendor_name = request_form.get('vendor_name')
        self.tin = request_form.get('tin')
        self.address = request_form.get('address')

    def validate_on_submit(self):
        self.errors = {}
        # Vendor Name
        if not self.vendor_name:
            self.errors["vendor_name"] = "Please type vendor name."
        else:
            existing_vendor = Vendor.query.filter(func.lower(Vendor.vendor_name) == func.lower(self.vendor_name), Vendor.id != self.id).first()
            if existing_vendor:
                self.errors["vendor_name"] = "Vendor already exists."

        # TIN
        existing_vendor = Vendor.query.filter(func.lower(Vendor.tin) == func.lower(self.tin), Vendor.id != self.id).first()
        if existing_vendor:
            self.errors["tin"] = "TIN already in use."

        if not self.errors:
            return True
        else:
            return False    
