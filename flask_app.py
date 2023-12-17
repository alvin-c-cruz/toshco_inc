from acas_auth import create_app
import ledger, payable_payment
from pathlib import Path

root = Path.cwd()
instance_folder = root / "instance"
template_folder = root / "templates"
blueprint_groups = (ledger, payable_payment)

app = create_app(
    instance_folder=instance_folder, 
    template_folder=template_folder, 
    blueprint_groups=blueprint_groups
    )

if __name__ == "__main__":
    app.run()