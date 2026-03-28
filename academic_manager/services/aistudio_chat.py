import os
import json
import requests
from academic_manager.config.settings import Config
from academic_manager.constants import get_full_prompt, get_basic_prompt

headers = {
    "Content-Type": "application/json",
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.MODEL}:generateContent"


def get_template_json(assignment: str, ignore_image: bool, project_name: str) -> str | None:
    """
    Generate a JSON template based on a given assignment and process the server's response.

    This function accepts an assignment, generates a corresponding prompt, sends it to a remote API,
    parses the response, and saves it to a file if it can be interpreted as JSON.

    :param project_name: The name of the project for which the template is generated.
    :param ignore_image: A boolean flag indicating whether to ignore image-related content in the assignment.
    :type ignore_image: bool
    :param assignment: A string input representing the assignment to generate the JSON template.
    :type assignment: str
    :return: A string containing the generated JSON template or None if an error occurs.
    """
    if not Config.API_KEY:
        raise ValueError("API_KEY não encontrada nas variáveis de ambiente")

    prompt = get_basic_prompt(assignment) if ignore_image else get_full_prompt(assignment)

    prompt_file_path = Config.BASE_DIR / project_name / "prompt.txt"
    with open(prompt_file_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            },
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
        }
    }

    headers.update({"X-goog-api-key": Config.API_KEY})

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code == 200:
        result = response.json()
        result_text = result["candidates"][0]["content"]["parts"][0]["text"]
        return result_text.replace("–", "-")
    else:
        print("Erro:", response.status_code)
        print(response.text)

    return None
