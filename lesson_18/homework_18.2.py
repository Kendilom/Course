import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='file.log',
    filemode='w'
)

import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8080"


def upload_image(image_path):
    image_path = Path(image_path)

    if not image_path.is_file():
        logger.error("File not exist")
        return None

    with open(image_path, "rb") as image:
        response = requests.post(
            f"{BASE_URL}/upload",
            files={"image": image}
        )

    if response.status_code == 201:
        image_url = response.json()["image_url"]
        logger.info(f"Image downloaded: {image_url}")
        return image_url

    logger.error(f"Downloading error: {response.status_code}")
    return None


def get_image_url(filename):
    response = requests.get(
        f"{BASE_URL}/image/{filename}",
        headers={"Content-Type": "text"}
    )

    if response.status_code == 200:
        image_url = response.json()["image_url"]
        logger.info(f"Image URL: {image_url}")
        return image_url

    logger.error(f"Cannot get image url: {response.status_code}")
    return None


def delete_image(filename):
    response = requests.delete(
        f"{BASE_URL}/delete/{filename}")

    if response.status_code == 200:
        logger.info(response.json()["message"])
        return True

    logger.error(f"Delete error: {response.status_code}")
    return False


if __name__ == "__main__":
    upload_image("image.jpg")
    get_image_url("image.jpg")
    delete_image("image.jpg")


