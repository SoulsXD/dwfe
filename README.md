git clone https://github.com/SoulsXD/dwfe.git
cd dwfe
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=flaskr
flask init-db ou flask --app flaskr init-db
flask run ou flask --app flaskr run
