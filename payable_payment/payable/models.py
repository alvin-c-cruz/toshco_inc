from acas_auth.application.extensions import db


class Payable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.String())
    ap_number = db.Column(db.String())
    
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    vendor = db.relationship('Vendor', backref='payables', lazy=True)

    invoice_number = db.Column(db.String())
    receiving_number = db.Column(db.String())
    po_number = db.Column(db.String())

    def amount_due(self):
        return 100
    
    def formatted_amount_due(self):
        return '{:,.2f}'.format(self.amount_due()) 
    
    def entry(self):
        return "In progress"


class PayableDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    payable_id = db.Column(db.Integer, db.ForeignKey('payable.id'), nullable=False)
    payable = db.relationship('Payable', backref='payable_details', lazy=True)

    quantity = db.Column(db.Float, default=0)
    
    measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'), nullable=False)
    measure = db.relationship('Measure', backref='payable_details', lazy=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='payable_details', lazy=True)
    
    unit_price = db.Column(db.Float, default=0)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='payable_details', lazy=True)


    sales_tax_id = db.Column(db.Integer, db.ForeignKey('sales_tax.id'), nullable=False)
    sales_tax = db.relationship('SalesTax', backref='payable_details', lazy=True)

    w_tax_id = db.Column(db.Integer, db.ForeignKey('w_tax.id'), nullable=False)
    w_tax = db.relationship('WTax', backref='payable_details', lazy=True)

    @property
    def formatted_quantity(self):
        return '{:,.0f}'.format(self.quantity)
    
    @property
    def amount(self):
        return self.quantity * self.unit_price
    
    @property
    def formatted_amount(self):
        return '{:,.2f}'.format(self.amount)
