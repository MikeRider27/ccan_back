import requests
from flask import current_app
from flask_restful import Resource


def get_access_token():
    url = f"{current_app.config['SUPERSET_URL']}/api/v1/security/login"
    body = {
        "username": current_app.config['SUPERSET_USERNAME'],
        "password": current_app.config['SUPERSET_PASSWORD'],
        "provider": "db",
        "refresh": True
    }
    response = requests.post(url=url, json=body)
    tokens = response.json()
    return tokens["access_token"], tokens["refresh_token"]


def refresh_access_token(refresh_token):
    url = f"{current_app.config['SUPERSET_URL']}/api/v1/security/refresh"
    headers = {"Authorization": f'Bearer {refresh_token}'}
    response = requests.post(url=url, headers=headers)
    token = response.json()
    return token["access_token"]


def get_csrf_token(access_token):
    url = f"{current_app.config['SUPERSET_URL']}/api/v1/security/csrf_token"
    headers = {"Authorization": f'Bearer {access_token}'}
    response = requests.get(url=url, headers=headers)
    csrf_token = response.json()
    return csrf_token.get('result')


class SupersetApi(Resource):
    def get(self):
        data = {
            'superset_url': current_app.config['SUPERSET_URL'],
            'superset_dashboard_id': current_app.config['SUPERSET_DASHBOARD_ID']
        }
        return data, 200

    def post(self):
        url = f"{current_app.config['SUPERSET_URL']}/api/v1/security/guest_token/"
        access_token, refresh_token = get_access_token()
        headers = {"Authorization": f'Bearer {access_token}'}
        body = {
            "resources": [
                {
                    "id": current_app.config['SUPERSET_DASHBOARD_ID'],
                    "type": "dashboard"
                }
            ],
            "rls": [
            ],
            "user": {
                "username": current_app.config['SUPERSET_USERNAME']
            }
        }
        response = requests.post(url=url, json=body, headers=headers)
        token = response.json()
        return token, 200


class Superset(Resource):
    def get(self):
        data = {
            'superset_url': current_app.config['SUPERSET_URL'],
            'superset_dashboard_id': current_app.config['SUPERSET_DASHBOARD_ID']
        }
        return data, 200