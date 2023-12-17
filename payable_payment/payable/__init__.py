app_name = "payable"
app_label = "Payables"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import Payable, PayableDetail
