app_name = "account_category"
app_label = "Account Category"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import AccountCategory
