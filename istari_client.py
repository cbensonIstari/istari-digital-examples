"""Istari Digital SDK client helper - reusable connection setup."""
import os
from dotenv import load_dotenv
from istari_digital_client import Client, Configuration

load_dotenv()

def get_client() -> Client:
    config = Configuration(
        registry_url=os.getenv("ISTARI_DIGITAL_REGISTRY_URL"),
        registry_auth_token=os.getenv("ISTARI_DIGITAL_REGISTRY_AUTH_TOKEN"),
    )
    return Client(config)

if __name__ == "__main__":
    client = get_client()
    user = client.get_current_user()
    print(f"Connected as: {user.display_name} ({user.email})")
