https://docs.digitalocean.com/tutorials/app-deploy-flask-app/

mkdir env
python3 -m venv env
source env/bin/activate

push to github main branch

create app for repo
update type, region, autodeploy?
edit run command
gunicorn --worker-tmp-dir /dev/shm app:app
