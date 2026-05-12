import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api")


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def login(email, password):
    return requests.post(
        f"{API_URL}/login",
        params={"email": email, "password": password}
    )


def get_service(service_id, token):
    return requests.get(
        f"{API_URL}/services/{service_id}",
        headers=get_headers(token)
    )


def create_service(data, token):
    return requests.post(
        f"{API_URL}/services",
        json=data,
        headers=get_headers(token)
    )


def create_reservation(data, token):
    return requests.post(
        f"{API_URL}/reservations",
        json=data,
        headers=get_headers(token)
    )

def get_services(token):
    return requests.get(
        f"{API_URL}/services",
        headers=get_headers(token)
    )


def get_users(token):
    return requests.get(
        f"{API_URL}/users",
        headers=get_headers(token)
    )
    
    
def get_reservations(token):
    return requests.get(
        f"{API_URL}/reservations",
        headers=get_headers(token)
    )