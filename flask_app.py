from acas_auth import create_app
import ledger, payable_payment, taxes
from pathlib import Path

root = Path.cwd()

# Pythonanywhere
instance_folder = root / "toshco_inc" / "instance"
template_folder = root / "toshco_inc" / "templates"
blueprint_groups = (ledger, payable_payment, taxes)

try:
    app = create_app(
        instance_folder=instance_folder,
        template_folder=template_folder,
        blueprint_groups=blueprint_groups
        )
except:
    pass

if __name__ == "__main__":
    #  For development
    instance_folder = root / "instance"
    template_folder = root /  "templates"

    app = create_app(
        instance_folder=instance_folder,
        template_folder=template_folder,
        blueprint_groups=blueprint_groups
        )

    app.run()