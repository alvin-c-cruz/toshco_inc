from acas_auth import create_app
import ledger, payable_payment, taxes
from pathlib import Path

root = Path.cwd()
print("Root Folder: ", root)
instance_folder = root / "toshco_inc" / "instance"
template_folder = root / "toshco_inc" / "templates"
blueprint_groups = (ledger, payable_payment, taxes)

app = create_app(
    instance_folder=instance_folder,
    template_folder=template_folder,
    blueprint_groups=blueprint_groups
    )

if __name__ == "__main__":
    app.run()