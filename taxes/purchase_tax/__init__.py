app_name = "purchase_tax"
app_label = "Purchase Tax"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import PurchaseTax
