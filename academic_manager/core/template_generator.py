import json
from pathlib import Path
from typing import Dict, Optional
from academic_manager.config.settings import Config
from academic_manager.core.file_manager import FileManager
from academic_manager.ui.interface import UserInterface
from academic_manager.services.aistudio_chat import get_template_json
from academic_manager.services.bing_images import process_json


class TemplateGenerator:
    """
    Provides static methods for generating templates using AI and selecting
    assignments for template generation. This utility class facilitates
    automation in generating and handling JSON templates based on assignment
    content and associated media data.
    """

    @staticmethod
    def generate_ai_template(
            assignment_content: str,
            media_data: Dict,
            output_path: Path,
            project_name: str
    ) -> Optional[Dict]:
        """
        Generates an AI template by formatting a provided template with given media data
        and writes it to a specified output path. If successfully completed, the function
        returns the resulting template data as a dictionary. If an error occurs during
        the process, it prints an error message and returns None.

        :param project_name: The name of the project for which the template is generated.
        :param assignment_content: The assignment content is used as input for generating
            the template.
        :type assignment_content: str
        :param media_data: A dictionary containing media-specific placeholder values to be
            injected into the template.
        :type media_data: Dict
        :param output_path: A Path object representing the desired output file location
            for the generated template.
        :type output_path: Path
        :return: The generated template data as a dictionary, or None if an error occurs
            during the process.
        :rtype: Optional[Dict]
        """
        try:
            print("Gerando template via IA...")
            ignore_image = not media_data and not Config.ENABLE_DOWNLOADS
            template_response = get_template_json(assignment_content, ignore_image, project_name)
            if Config.ENABLE_DOWNLOADS:
                json_data = json.loads(template_response)
                media_data = process_json(json_data, project_name)
            template_formatted = template_response.replace("–", "-") % media_data

            template_data = json.loads(template_formatted)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)

            print(f"✓ Template gerado: {output_path.name}")
            return template_data

        except json.JSONDecodeError as e:
            print(f"Erro ao processar JSON do template: {e}")
        except Exception as e:
            print(f"Erro ao gerar template: {e}")

        return None

    @staticmethod
    def select_assignment() -> Optional[str]:
        """
        Selects an assignment from a list of available assignments and reads its content.

        The method fetches the list of available assignments, prompts the user
        to select one, and reads the content of the selected assignment file.

        :rtype: Optional[str]
        :return: The content of the selected assignment if successfully read, or
            None if no assignment is selected or the file could not be read.
        """
        assignments = FileManager.list_assignments()
        selected = UserInterface.select_from_list(assignments, "Enunciados disponíveis")

        if not selected:
            return None

        assignment_path = Config.ASSIGNMENTS_DIR / selected
        try:
            with open(assignment_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler enunciado: {e}")
            return None
