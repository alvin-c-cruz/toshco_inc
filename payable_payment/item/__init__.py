app_name = "item"
app_label = "Item"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import Item
