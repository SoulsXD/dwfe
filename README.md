git clone https://github.com/SoulsXD/dwfe.git
cd dwfe
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "flaskr"
flask init-db
flask run
