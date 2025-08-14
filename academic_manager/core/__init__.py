import json
from typing import Dict, Optional
from academic_manager.config.settings import Config
from academic_manager.core.file_manager import FileManager
from academic_manager.core.template_generator import TemplateGenerator
from academic_manager.core.pdf_generator import PDFGenerator
from academic_manager.core.project_manager import ProjectManager
from academic_manager.ui.interface import UserInterface


class AcademicManager:
    """
    Manages and automates the process of academic project creation and updates.

    The `AcademicProjectManager` class facilitates the generation of academic project
    templates and corresponding PDFs. It integrates with components such as a project
    manager, a template generator, and a PDF generator to streamline the workflow. The
    class also allows for user interaction to customize the project creation process.

    :ivar project_manager: Manages the creation and updating of academic projects.
    :type project_manager: ProjectManager
    :ivar template_generator: Handles generating and managing project templates.
    :type template_generator: TemplateGenerator
    :ivar pdf_generator: Responsible for generating PDF outputs for projects.
    :type pdf_generator: PDFGenerator
    """
    def __init__(self, *args, **kwargs):
        self.project_manager = ProjectManager()
        self.template_generator = TemplateGenerator()
        self.pdf_generator = PDFGenerator()

    def _handle_template_generation(self, project_name: str, metadata: Dict) -> Optional[Dict]:
        """
        Handles the generation of a project template based on user input or default settings.

        This method determines the appropriate template for the given project either by using
        a default template, generating an AI-based template, or loading an existing template
        from a file. The decision is based on the project name and user input.

        :param project_name: The name of the project to generate a template for.
        :param metadata: Metadata associated with the project, containing details required for
            template generation (e.g., title information).
        :return: A dictionary representing the chosen template, or None if the operation is
            canceled by the user.
        """
        if project_name.startswith("project_"):
            return Config.DEFAULT_TEMPLATE

        choice = UserInterface.get_user_choice(
            "Deseja gerar template via IA (1) ou usar template padrão (2)?",
            ['1', '2']
        )

        if choice == 'q':
            return None

        if choice == '1':
            return self._generate_ai_template(project_name, metadata)
        else:
            filename = metadata["titulo"].replace(" ", "_").capitalize()
            template_file = Config.BASE_DIR / project_name / f"{filename}.json"
            with open(template_file, "r", encoding="utf-8") as f:
                existing_template = json.load(f)

            if not existing_template:
                print(f'\n✓ Carregando template Padrão')
                return Config.DEFAULT_TEMPLATE

            print(f'\n✓ Carregando template: {template_file.name}')
            return existing_template

    def _generate_ai_template(self, project_name: str, metadata: Dict) -> Optional[Dict]:
        """
        Generates an AI-based template for a given project using metadata and media data.

        This function uses the provided project name and metadata to prepare media data
        from the project's attachments. The AI template generator is then utilized to
        create a template based on selected assignment content and media information.

        :param project_name: The name of the project for which the template is generated
        :param metadata: A dictionary containing metadata such as project-specific
                         information
        :return: A dictionary representing the generated template if successful, or None
                 if no assignment content is selected
        """
        assignment_content = self.template_generator.select_assignment()
        if not assignment_content:
            print("Nenhum enunciado selecionado.")
            return None

        attachments = FileManager.list_attachments(project_name)
        media_data = {}

        for idx, attachment in enumerate(attachments):
            attachment_path = Config.BASE_DIR / project_name / "attachments" / attachment
            media_data[f"imagem_{idx + 1}"] = str(attachment_path)

        filename = metadata["titulo"].replace(" ", "_").capitalize()
        template_path = Config.BASE_DIR / project_name / f"{filename}.json"

        return self.template_generator.generate_ai_template(
            assignment_content,
            media_data,
            template_path,
            project_name
        )

    def run(self):
        """
        Controls the main flow for generating and managing academic projects and their reports.
        The method provides interaction with the user to create or update projects, then collects project
        metadata, generates corresponding templates, and proceeds to generate a final PDF report.

        :return: None
        """
        print("=== Sistema de Geração de Trabalhos Acadêmicos ===\n")

        while True:
            choice = UserInterface.get_user_choice(
                "Criar novo projeto (1) ou atualizar existente (2)?",
                ['1', '2']
            )

            if choice == 'q':
                print("Saindo do sistema.")
                break

            if choice is None:
                continue

            if choice == '1':
                result = self.project_manager.create_new_project()
            else:
                result = self.project_manager.update_existing_project()

            if not result:
                continue

            project_name, metadata = result
            print(f"\nMetadados do projeto:\n{json.dumps(metadata, indent=2, ensure_ascii=False)}")

            template = self._handle_template_generation(project_name, metadata)
            if not template:
                continue

            if self.pdf_generator.generate_pdf(project_name, metadata, template):
                print("\n✓ Processo concluído com sucesso!")

            print("\n" + "=" * 50 + "\n")
