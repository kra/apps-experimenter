# Setup

- have apps-experimenter repo with dev branch on github
- add app-dev.phu73l.net DigitalOcean domain
- have config.yaml containing "access-token: <token>"

# Set up dev instance

To be done once.

Copy .do/app.yaml.template to .do/app.yaml, and substitue GOOGLE_CREDS_JSON.

Create the app, note the id.

    doctl --config config.yaml apps create --spec .do/app.yaml
    
Deploy the app by updating it.

    doctl --config config.yaml apps update <id> --spec .do/app.yaml 

Get the hostname from the "Default Ingress" field of the app.

    doctl --config config.yaml apps list <id>

Add CNAME for ws.app-dev.phu73l.net pointing to the app's hostname in DigitalOcean domain. Wait for the domain status to resolve in settings.

# Deploy dev instance

## Update source

If source has changed, push to apps-experimenter dev branch on github.

## Update config

If .do/app.yaml has changed, update config.

Get the app ID.

    doctl --config config.yaml apps list

Update config.

    doctl --config config.yaml apps update <id> --spec .do/app.yaml 

# Delete dev instance

Get the app ID.

    doctl --config config.yaml apps list

Delete the app.

    doctl --config config.yaml apps delete <id>

# Unit test

## Setup

To be done once.

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt

## Test

    python3 -m unittest discover -s test

# Smoke test setup

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt

## Smoke test

    gunicorn --worker-tmp-dir /dev/shm --config gunicorn_config.py webserver:app

    export google_creds_json=XXX && python server.py

# Smoke integration test

hit the URL on the web GUI page e.g.

    wget --post-data "foo=bar" https://ws.app-dev.phu73l.net/twiml

# Notes

https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main
