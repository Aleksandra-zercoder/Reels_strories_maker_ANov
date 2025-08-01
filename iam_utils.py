import requests
import json
import time
import os
from config import OAUTH_TOKEN, IAM_TOKEN

def update_iam_token():
    try:
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        headers = {"Content-Type": "application/json"}
        data = {"yandexPassportOauthToken": OAUTH_TOKEN}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        iam_token = response.json().get("iamToken")

        os.makedirs(os.path.dirname(IAM_TOKEN), exist_ok=True)
        with open(IAM_TOKEN, "w") as f:
            json.dump({"iam_token": iam_token}, f)

        print("✅ IAM-токен успешно обновлён")
        return iam_token
    except Exception as e:
        print(f"❌ Ошибка при обновлении IAM-токена: {e}")
        return None


def get_iam_token():
    if not os.path.exists(IAM_TOKEN):
        return update_iam_token()

    with open(IAM_TOKEN, "r") as f:
        data = json.load(f)
        return data.get("iam_token")
