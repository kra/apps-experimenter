# Setup

- have apps-experimenter repo with dev branch on github
- add app-dev.phu73l.net DigitalOcean domain
- have config.yaml containing "access-token: <token>"

# Set up dev instance

To be done once.

    doctl --config config.yaml apps create --spec .do/app.yaml

Add CNAME for ws.app-dev.phu73l.net pointing to app host in DigitalOcean domain. Wait for domain status to resolve in settings.

# Deploy dev instance

If source has changed, push to apps-experimenter dev branch on github.

If config in .do directory has changed, update config.

Get app ID.

    doctl --config config.yaml apps list

Update config.

    doctl --config config.yaml apps update <id> --spec .do/app.yaml 

# Test

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt
- gunicorn --worker-tmp-dir /dev/shm --config gunicorn_config.py webserver:app

# Smoke

hit the URL on the web GUI page e.g.

    wget --post-data "foo=bar" https://ws.app-dev.phu73l.net/twiml

# Notes

https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main
