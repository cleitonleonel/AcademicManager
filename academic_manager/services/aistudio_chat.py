import time
import requests
from academic_manager.config.settings import Config
from academic_manager.constants import get_full_prompt, get_basic_prompt

# Modelo alternativo caso o principal enfrente sobrecarga
FALLBACK_MODEL = getattr(Config, "FALLBACK_MODEL", "gemini-2.5-flash")


def _execute_request(model_name: str, api_key: str, prompt: str, timeout: int = 90) -> str | None:
    """Executa a chamada HTTP com configuração de thinking reduzida e timeout explícito."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }

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
            # Limita o overhead de raciocínio no 3.8
            "thinkingConfig": {
                "thinkingLevel": "LOW"
            }
        }
    }

    # Se for o fallback ou um modelo legado que não use thinkingLevel, remove o bloco se der 400
    try:
        response = requests.post(url, headers=headers, json=body, timeout=timeout)

        # Caso o modelo secundário rejeite o thinkingConfig
        if response.status_code == 400 and "thinking" in response.text.lower():
            body["generationConfig"].pop("thinkingConfig", None)
            response = requests.post(url, headers=headers, json=body, timeout=timeout)

        if response.status_code == 200:
            result = response.json()
            result_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return result_text.replace("–", "-")

        print(f"[{model_name}] Erro HTTP {response.status_code}: {response.text}")
        return None

    except requests.exceptions.Timeout:
        print(f"[{model_name}] Timeout após {timeout}s.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[{model_name}] Erro de rede/requisição: {e}")
        return None


def get_template_json(
        assignment: str,
        ignore_image: bool,
        project_name: str,
        api_key_override: str = None,
        max_retries: int = 3
) -> str | None:
    api_key = api_key_override or Config.API_KEY
    if not api_key:
        raise ValueError("API_KEY não encontrada nas variáveis de ambiente ou na requisição")

    prompt = get_basic_prompt(assignment) if ignore_image else get_full_prompt(assignment)

    prompt_file_path = Config.BASE_DIR / project_name / "prompt.md"
    with open(prompt_file_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    # 1. Tentativas no modelo primário (ex: gemini-3.8-flash) com Exponential Backoff
    for attempt in range(max_retries):
        result = _execute_request(
            model_name=Config.MODEL,
            api_key=api_key,
            prompt=prompt,
            timeout=75
        )
        if result:
            return result

        wait_seconds = 2 ** attempt
        print(f"Tentativa {attempt + 1} falhou. Aguardando {wait_seconds}s para retentar...")
        time.sleep(wait_seconds)

    # 2. Fallback caso o modelo primário continue inacessível/sobrecarregado
    print(f"Tentando modelo secundário ({FALLBACK_MODEL})...")
    fallback_result = _execute_request(
        model_name=FALLBACK_MODEL,
        api_key=api_key,
        prompt=prompt,
        timeout=45
    )
    if fallback_result:
        return fallback_result

    print("Todas as tentativas e fallbacks falharam.")
    return None
