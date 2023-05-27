# setup

push to apps-experimenter dev branch on github

# deploy

- create app
- repo apps-experimenter branch dev
- autodeploy
- region sfo
- plan basic
- create

# test

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt
- gunicorn --worker-tmp-dir /dev/shm --config gunicorn_config.py webserver:app

# smoke

hit the URL on the web GUI page e.g.

    wget --post-data "foo=bar" https://seal-app-3ypy4.ondigitalocean.app/twiml

# notes

https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main
