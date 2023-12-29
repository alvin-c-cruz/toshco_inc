app_name = "sales_tax"
app_label = "Sales Tax"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import SalesTax
