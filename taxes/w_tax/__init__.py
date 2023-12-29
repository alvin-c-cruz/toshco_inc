app_name = "w_tax"
app_label = "Withholding Tax"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import WTax
