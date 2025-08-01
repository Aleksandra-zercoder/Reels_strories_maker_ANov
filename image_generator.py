import requests
import base64
import time
import os
from iam_utils import get_iam_token
from config import FOLDER_ID

def generate_image(prompt, output_path="generated/generated_image.jpeg"):
    iam_token = get_iam_token()

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "x-folder-id": FOLDER_ID,
        "Content-Type": "application/json"
    }

    payload = {
        "modelUri": f"art://{FOLDER_ID}/yandex-art/latest",
        "generationOptions": {
            "seed": 1863,
            "aspectRatio": {"widthRatio": "9", "heightRatio": "16"}
        },
        "messages": [{"weight": "1", "text": prompt}]
    }

    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync",
                             headers=headers, json=payload)
    response.raise_for_status()
    request_id = response.json().get("id")

    time.sleep(10)  # ⏳ ждём генерацию

    result_url = f"https://llm.api.cloud.yandex.net/operations/{request_id}"
    result_response = requests.get(result_url, headers=headers)
    result_response.raise_for_status()
    image_base64 = result_response.json().get("response", {}).get("image")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(image_base64))

    print(f"✅ Изображение сохранено: {output_path}")
    return output_path

