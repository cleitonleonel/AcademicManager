import os
import json
import requests
from academic_manager.config.settings import Config
from academic_manager.constants import get_full_prompt, get_basic_prompt

headers = {
    "Content-Type": "application/json",
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.MODEL}:generateContent"


def get_template_json(
        assignment: str,
        ignore_image: bool,
        project_name: str,
        api_key_override: str = None
) -> str | None:
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
    api_key = api_key_override or Config.API_KEY
    if not api_key:
        raise ValueError("API_KEY não encontrada nas variáveis de ambiente ou na requisição")

    prompt = get_basic_prompt(assignment) if ignore_image else get_full_prompt(assignment)

    prompt_file_path = Config.BASE_DIR / project_name / "prompt.md"
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

    headers.update({"X-goog-api-key": api_key})

    try:
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
    except Exception as e:
        print(f"Erro na chamada da API: {e}")

    return None
