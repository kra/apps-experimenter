https://docs.digitalocean.com/tutorials/app-deploy-flask-app/

mkdir env
python3 -m venv env
source env/bin/activate
pip install Flask gunicorn
pip freeze >requirements.txt
