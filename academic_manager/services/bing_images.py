import os
import re
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
from academic_manager.config.settings import Config

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/115.0.0.0 Safari/537.36"
}

def get_image_url(query):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[X] Erro ao acessar Bing para a consulta: {query}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    image_links = soup.find_all("a", class_="iusc")
    for img in image_links:
        m = img.get("m")
        if m:
            urls = re.findall(r'"murl":"(.*?)"', m)
            if urls:
                return urls[0].replace("\\", "")
    return None

def download_image(url, path):
    try:
        image_data = requests.get(url, headers=HEADERS, timeout=10).content
        with open(path, "wb") as f:
            f.write(image_data)
        print(f"[OK] Imagem salva: {path}")
    except Exception as e:
        print(f"[X] Erro ao baixar a imagem: {e}")

def process_json(json_data: dict, project_name: str):
    """
    Processes the given JSON data to download images based on descriptions provided in the data structure
    and organizes them in a defined directory structure.

    The function iterates through sections and blocks in the provided JSON data, identifies blocks
    of type 'image', and uses their description to search for corresponding images. The images are
    downloaded to a specified destination directory, organized by project name.

    :param json_data: Dictionary containing structured JSON data with sections, blocks, and image details.
    :type json_data: dict
    :param project_name: The name of the project, which determines the destination directory for images.
    :type project_name: str
    :return: A dictionary mapping placeholders to file paths for successfully downloaded images, or
             empty strings for images that could not be found.
    :rtype: dict
    """

    image_dest = Config.BASE_DIR / project_name / "attachments"
    media_data = {}
    count = 1
    for section in json_data.get("sections", []):
        for block in section.get("blocks", []):
            if block.get("type") == "image":
                description = block.get("text", "")
                placeholder = f"imagem_{count}"
                print(f"[>] Buscando imagem para: {description}")
                image_url = get_image_url(description)
                if image_url:
                    final_path = os.path.join(image_dest, f"{placeholder}.jpg")
                    download_image(image_url, final_path)
                    media_data[placeholder] = final_path
                    count += 1
                    time.sleep(1)
                else:
                    print(f"[X] Nenhuma imagem encontrada para: {description}")
                    media_data[placeholder] = ""

    return media_data

