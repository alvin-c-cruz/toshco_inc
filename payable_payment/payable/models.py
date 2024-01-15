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

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='payables', lazy=True)    

    def amount_due(self):
        balance = 0
        for detail in self.payable_details:
            balance += detail.net()['amount_due']
        return balance
    
    def formatted_amount_due(self):
        return '{:,.2f}'.format(self.amount_due()) 
    
    def entry(self):
        entries = []
        for detail in self.payable_details:
            entries.append(detail.entry())
        return entries


class PayableDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    payable_id = db.Column(db.Integer, db.ForeignKey('payable.id'), nullable=False)
    payable = db.relationship('Payable', backref='payable_details', lazy=True)

    quantity = db.Column(db.Float, default=0)
    
    measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'), nullable=False)
    measure = db.relationship('Measure', backref='payable_details', lazy=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='payable_details', lazy=True)
    
    amount = db.Column(db.Float, default=0)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='payable_details', lazy=True)

    purchase_tax_id = db.Column(db.Integer, db.ForeignKey('purchase_tax.id'), nullable=False)
    purchase_tax = db.relationship('PurchaseTax', backref='payable_details', lazy=True)

    purchase_w_tax_id = db.Column(db.Integer, db.ForeignKey('purchase_w_tax.id'), nullable=False)
    purchase_w_tax = db.relationship('PurchaseWTax', backref='payable_details', lazy=True)

    @property
    def formatted_quantity(self):
        return '{:,.0f}'.format(self.quantity)
        
    def __str__(self):
        return f"{self.quantity} {self.measure.measure_name} of {self.item.item_name} for {self.amount}"
    
    def net(self):
        vat = round(self.amount / (1 + (self.purchase_tax.vat_rate())) * self.purchase_tax.vat_rate(), 2)
        net_of_vat = self.amount - vat
        ewt = round(net_of_vat * self.purchase_w_tax.wt_rate(), 2)
        amount_due = self.amount - ewt

        return {
            "net_of_vat": net_of_vat,
            "vat": vat,
            "ewt": ewt,
            "amount_due": amount_due
        }

        
    def entry(self):
        debits = []
        credits = []

        net = self.net()

        # Tax Base
        debits.append(
            {
                "account": self.account,
                "amount": net['net_of_vat']
            }
        )

        # VAT
        if net['vat']:
            debits.append(
                {
                    "account": self.purchase_tax.account,
                    "amount": net['vat']
                }
            )

        # EWT
        if net['ewt']:
            credits.append(
                {
                    "account": self.purchase_w_tax.account,
                    "amount": net['ewt']
                }
            )

        # AMOUNT DUE account is added in the accumulated entry in main model
        credits.append(
            {
                "amount": net['amount_due']
            }
        )


        return {
            "debits": debits,
            "credits": credits
        }
