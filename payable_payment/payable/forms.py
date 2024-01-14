from dataclasses import dataclass
from sqlalchemy import func
from acas_auth.application.extensions import db
from .models import Payable, PayableDetail


DETAIL_ROWS = 10


@dataclass
class SubForm:
    id: int = 0
    payable_id:int = 0
    quantity: float = 0
    amount: float = 0
    measure_id: int = 0
    item_id: int = 0
    account_id: int = 0
    purchase_tax_id: int = 0
    purchase_w_tax_id: int = 0

    errors = {}

    def validate(self):
        self.errors = {}

        if self.is_dirty():
            if self.quantity <= 0:
                self.errors["quantity"] = "Quantity should be greater than zero (0)."

            if self.amount < 0:
                self.errors["amount"] = "Amount cannot be negative."

            if not self.measure_id:
                self.errors["measure_id"] = "Please select measure."

            if not self.item_id:
                self.errors["item_id"] = "Please select item."

            if not self.account_id:
                self.errors["account_id"] = "Please select account."

            if not self.purchase_tax_id:
                self.errors["purchase_tax_id"] = "Please select purchase tax."

            if not self.purchase_w_tax_id:
                self.errors["purchase_w_tax_id"] = "Please select w/tax."

        if not self.errors:
            return True
        else:
            return False    

    def is_dirty(self):
        return any([self.quantity, self.amount, self.measure_id, self.item_id, self.account_id, self.purchase_tax_id, self.purchase_w_tax_id])    
        

@dataclass
class Form:
    id: int = None
    record_date: str = ""
    ap_number: str = ""
    vendor_id: int = 0
    invoice_number: str = ""
    receiving_number: str = ""
    po_number: str = ""
    account_id: int = 0

    details = []
    errors = {}

    def __post_init__(self):
        self.details = []
        for i in range(DETAIL_ROWS):
            self.details.append((i, SubForm()))

    def save(self):
        if self.id is None:
            # Add a new record
            new_record = Payable(
                record_date=self.record_date,
                ap_number=self.ap_number,
                vendor_id=self.vendor_id,
                invoice_number=self.invoice_number,
                receiving_number=self.receiving_number,
                po_number=self.po_number,
                account_id=self.account_id
                )
            db.session.add(new_record)
            db.session.commit()

            for _, detail in self.details:
                if detail.is_dirty():
                    new_detail = PayableDetail(
                        payable_id=new_record.id,
                        quantity=detail.quantity,
                        amount=detail.amount,
                        measure_id=detail.measure_id,
                        item_id=detail.item_id,
                        account_id=detail.account_id,
                        purchase_tax_id=detail.purchase_tax_id,
                        purchase_w_tax_id=detail.purchase_w_tax_id
                    )
                    db.session.add(new_detail)
                    db.session.commit()

        else:
            # Update an existing record
            record = Payable.query.get(self.id)
            if record:
                record.record_date = self.record_date
                record.ap_number = self.ap_number
                record.vendor_id = self.vendor_id
                record.invoice_number = self.invoice_number
                record.receiving_number = self.receiving_number
                record.po_number = self.po_number
                record.account_id = self.account_id
                
                details = PayableDetail.query.filter(PayableDetail.payable_id==self.id)
                for detail in details:
                    db.session.delete(detail)

                for _, detail in self.details:
                    if detail.is_dirty():
                        row_detail = PayableDetail(
                            payable_id=record.id,
                            quantity=detail.quantity,
                            amount=detail.amount,
                            measure_id=detail.measure_id,
                            item_id=detail.item_id,
                            account_id=detail.account_id,
                            purchase_tax_id=detail.purchase_tax_id,
                            purchase_w_tax_id=detail.purchase_w_tax_id
                            )
                        db.session.add(row_detail)
                
        db.session.commit()
   
    def post(self, request_form):
        self.id = request_form.get('payable_id')
        self.record_date = request_form.get('record_date')
        self.ap_number = request_form.get('ap_number')
        self.vendor_id = int(request_form.get('vendor_id'))
        self.invoice_number = request_form.get('invoice_number')
        self.receiving_number = request_form.get('receiving_number')
        self.po_number = request_form.get('po_number')
        self.account_id = int(request_form.get('account_id'))

        for i in range(DETAIL_ROWS):
            if type(request_form.get(f'quantity-{i}')) == str:
                quantity_value = request_form.get(f'quantity-{i}')
                if quantity_value.isnumeric() or (quantity_value.replace('.', '', 1).isdigit() and quantity_value.count('.') <= 1):
                    self.details[i][1].quantity = float(quantity_value)
                else:
                    self.details[i][1].quantity = 0
            else: 
                self.details[i][1].quantity = request_form.get(f'quantity-{i}')

            self.details[i][1].measure_id = int(request_form.get(f'measure_id-{i}'))

            if type(request_form.get(f'amount-{i}')) == str:
                amount_value = request_form.get(f'amount-{i}')
                if amount_value.isnumeric() or (amount_value.replace('.', '', 1).isdigit() and amount_value.count('.') <= 1):
                    self.details[i][1].amount = float(amount_value)
                else:
                    self.details[i][1].amount = 0
            else: 
                self.details[i][1].amount = request_form.get(f'amount-{i}')

            self.details[i][1].item_id = int(request_form.get(f'item_id-{i}'))
            self.details[i][1].account_id = int(request_form.get(f'account_id-{i}'))
            self.details[i][1].purchase_tax_id = int(request_form.get(f'purchase_tax_id-{i}'))
            self.details[i][1].purchase_w_tax_id = int(request_form.get(f'purchase_w_tax_id-{i}'))

    def validate_on_submit(self):
        self.errors = {}
        detail_validation = True

        if not self.record_date:
            self.errors["record_date"] = "Please type date."

        if not self.ap_number:
            self.errors["ap_number"] = "Please type reference number."
        else:
            duplicate = Payable.query.filter(func.lower(Payable.ap_number) == func.lower(self.ap_number), Payable.id != self.id).first()
            if duplicate:
                self.errors["ap_number"] = "Reference is already used, please verify."        

        if not self.vendor_id:
            self.errors["vendor_id"] = "Please select vendor."

        if not self.account_id:
            self.errors["account_id"] = "Please select payable account."

        for i in range(DETAIL_ROWS):
            if not self.details[i][1].validate():
                detail_validation = False

        all_not_dirty = True
        for _, detail in self.details:
            if detail.is_dirty():
                all_not_dirty = False

        if all_not_dirty:
            self.errors["entry"] = "There should be at least one entry."       

        if not self.errors and detail_validation:
            return True        
