def get_full_prompt(assignment: str) -> str:
    """
    Generates a prompt string for creating a structured academic work JSON with
    specific formatting guidelines. Depending on the value of the `ignore_image`
    parameter, images might be included or excluded from the output JSON format.

    :param assignment: Academic work assignment which is used as input for generating
        the JSON prompt. The assignment should contain all relevant details for
        structuring the academic work.
    :type assignment: str
    :returns: A formatted prompt for generating a JSON structured academic work.
    :rtype: str
    """
    prompt = f"""
    Você é um aluno e seu professor passa um trabalho avaliativo com o seguinte enunciado:
    
    {assignment}
     
    Sua tarefa é pesquisar por conteúdos relacionandos e retornar **somente** um JSON estruturado no seguinte formato:
    
    {{
      "title": "Título do trabalho",
      "sections": [
        {{
          "name": "Nome da seção",
          "blocks": [
            {{
              "type": "paragraph",
              "text": "Texto do parágrafo"
            }},
            {{
              "type": "subtitle",
              "text": "Texto do subtítulo",
              "align": "L" | "C" | "R" | "J",
              "font": {{
                "style": "B" | "I" | "U" | "BI" | "BU" | "IB",
                "size": número_em_porcentagem_relativa_ao_pdf (padrão 12 se não especificado)
              }}
            }},
            {{
              "type": "image",
              "position": "left" | "right" | "above" | "below",
              "path": numero_da_imagem (ex: %(imagem_1)s, %(imagem_2)s, etc.) no máximo 3 .,
              "width": número_em_porcentagem_relativa_ao_pdf (padrão 100 se não especificado) obrigatório para todas as imagens,
              "height": número_em_porcentagem_relativa_ao_pdf (padrão 80 se não especificado) obrigatório para todas as imagens,
              "text": "Legenda ou texto explicativo da imagem"
            }},
            {{
              "type": "list",
              "items": [
                "Item 1",
                "Item 2",
                "... etc."
              ]
            }}
          ]
        }}
      ]
    }}
    
    ---
    
    Segue um modelo de layout para o JSON estruturado:
    
    ------------------------------------------------------------
    - Modelo do layout:
    ------------------------------------------------------------
    [Texto introdutório acima]
    [IMAGEM_1 left] Texto explicativo da imagem 1
    ------------------------------------------------------------
    Texto explicativo da imagem 2       [IMAGEM_2 right]
    ------------------------------------------------------------
    [IMAGEM_3 left] Texto explicativo da imagem 3
    ------------------------------------------------------------
    Texto explicativo da imagem 4       [IMAGEM_4 right]
    ------------------------------------------------------------
    [Texto explicativo final acima]
                     [IMAGEM_5 below]]
    ------------------------------------------------------------
    
    ---
    
    Gere o JSON seguindo rigorosamente este formato.
    """
    return prompt


def get_basic_prompt(assignment: str) -> str:
    """
    Generates a formatted string prompt to guide the structuring of a JSON response
    based on a given academic work assignment. This prompt is specifically designed
    to enforce a well-structured JSON output as described in the format details within
    the function logic.

    :param assignment: The academic work assignment text to be formatted within the
        prompt. The content should be provided as a single cohesive string.
    :type assignment: str
    :return: A string containing the detailed instructions for constructing the JSON
        response. The string outlines the required structure in a precise format.
    :rtype: str
    """
    prompt = f"""
    {assignment}
     
    Sua tarefa é pesquisar por conteúdos relacionandos e retornar **somente** um JSON estruturado no seguinte formato:
    
    {{
      "title": "Título do trabalho",
      "sections": [
        {{
          "name": "Nome da seção",
          "blocks": [
            {{
              "type": "paragraph",
              "text": "Texto do parágrafo"
            }},
            {{
              "type": "subtitle",
              "text": "Texto do subtítulo",
              "align": "L" | "C" | "R" | "J",
              "font": {{
                "style": "B" | "I" | "U" | "BI" | "BU" | "IB",
                "size": número_em_porcentagem_relativa_ao_pdf (padrão 12 se não especificado)
              }}
            }},
            {{
              "type": "list",
              "items": [
                "Item 1",
                "Item 2",
                "... etc."
              ]
            }}
          ]
        }}
      ]
    }}
    
    ---
    
    Gere o JSON seguindo rigorosamente este formato.
    """
    return prompt
