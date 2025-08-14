import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from academic_manager.config.settings import Config
from academic_manager.core.file_manager import FileManager
from academic_manager.ui.interface import UserInterface


class ProjectManager:
    """
    Handles operations related to project creation and management.

    This class provides functionality to create and update projects with a hierarchical
    directory structure, associated metadata, and default files. It interacts with
    other modules for managing files and user interaction. The class ensures all
    necessary directories exist and helps maintain consistency while managing projects.

    """

    def __init__(self):
        """
        Ensures that the required directories exist for handling file management tasks.
        This is executed during the initialization of the class.

        Ensures that all essential directories required by the application
        are checked for existence and created if not present.

        """
        FileManager.ensure_directories_exist()

    def _get_next_project_number(self) -> int:
        """
        Calculate the next available project number based on existing projects.

        This function retrieves the list of existing projects, identifies project directories
        that follow the naming convention "project_<number>", extracts the numerical part
        from those names, and determines the next available project number. If no such
        projects exist, it defaults to 1.

        :return: The next available project number.
        :rtype: int
        """
        existing_projects = FileManager.list_projects()
        project_numbers = [
            int(p.split("_")[1]) for p in existing_projects
            if p.startswith("project_") and len(p.split("_")) > 1 and p.split("_")[1].isdigit()
        ]
        return max(project_numbers, default=0) + 1

    def _create_project_structure(self, project_path: Path) -> None:
        """
        Creates the directory structure for a project.

        This function ensures the creation of the main project directory and its
        subdirectories, such as 'sources' and 'attachments'. It also copies default
        source files (e.g., 'mask.png', 'logo.png') from a predefined static path
        to the 'sources' directory of the project.

        :param project_path: The path where the project structure will be created.
        :type project_path: Path
        :raises OSError: If there is an error during directory or file creation.
        """
        project_path.mkdir(exist_ok=True)
        (project_path / "sources").mkdir(exist_ok=True)
        (project_path / "attachments").mkdir(exist_ok=True)

        source_files = ['mask.png', 'logo.png']
        for file in source_files:
            src = Path('static') / 'img' / file
            dst = project_path / 'sources' / file
            if src.exists():
                shutil.copy2(src, dst)

    def _save_project_files(self, project_path: Path, metadata: Dict) -> None:
        """
        Saves project metadata and default instructions to the provided project directory.

        :param project_path: The file system path where the project files will be saved.
        :param metadata: A dictionary containing the project metadata to be written in
            a JSON file within the project directory.
        :return: None
        """
        settings_file = project_path / "settings.json"
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)

        instructions_file = project_path / "instructions.md"
        with open(instructions_file, "w", encoding="utf-8") as f:
            f.write(Config.DEFAULT_INSTRUCTIONS)

    def _collect_metadata(self, existing_metadata: Optional[Dict] = None) -> Dict:
        """
        Collects and updates metadata for a project interactively.

        This function takes an optional existing metadata dictionary, either copying
        its contents or initializing a new dictionary if none is provided. It prompts
        the user for input to update each key based on default values or available
        current values. The year key is automatically set to the current year.

        :param existing_metadata: Optional dictionary containing existing metadata values.
                                  If provided, its content will be used as the base for
                                  updates. If not provided, a new dictionary will be
                                  initialized.
        :type existing_metadata: Optional[Dict]
        :return: A dictionary containing the final metadata with user updates.
        :rtype: Dict
        """
        metadata = existing_metadata.copy() if existing_metadata else {}

        print("\nPreencha os dados do projeto (pressione ENTER para manter o valor atual):")

        for key, default_value in Config.DEFAULT_METADATA.items():
            if key == "ano":
                metadata[key] = datetime.now().year
                continue

            current_value = metadata.get(key, default_value)
            metadata[key] = UserInterface.input_with_default(key.capitalize(), str(current_value))

        return metadata

    def create_new_project(self) -> Optional[Tuple[str, Dict]]:
        """
        Creates a new project with a specific name and default structure, based on
        user input or a default naming convention. This method ensures that the new
        project is properly initialized with the required metadata and saved in a
        predetermined location. Any errors encountered during the creation process
        will result in an unsuccessful attempt notification and a `None` return value.

        :return: A tuple containing the name of the created project and its associated
            metadata, or `None` if an error occurs.
        :rtype: Optional[Tuple[str, Dict]]
        """
        next_number = self._get_next_project_number()
        default_name = f"project_{str(next_number).zfill(3)}"

        project_name = UserInterface.input_with_default("Nome do projeto", default_name)
        project_path = Config.BASE_DIR / project_name.replace(" ", "_")

        try:
            self._create_project_structure(project_path)
            metadata = self._collect_metadata()
            self._save_project_files(project_path, metadata)

            print(f"\n✓ Novo projeto criado: {project_name}")
            return project_name, metadata

        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            return None

    def update_existing_project(self) -> Optional[Tuple[str, Dict]]:
        """
        Updates metadata of an existing project.

        This method allows updating the configuration of an existing project. The user is
        prompted to select a project from a list of available ones. Once a project is selected,
        its settings file is loaded, metadata is updated based on provided input, and the file
        is saved back. If any issues occur during this process, appropriate error messages
        are displayed, and the update operation may fail.

        :return: A tuple containing the selected project's name and the updated metadata if
            the operation is successful, or None if the operation fails or is canceled.
        :rtype: Optional[Tuple[str, Dict]]
        """
        projects = FileManager.list_projects()
        selected_project = UserInterface.select_from_list(projects, "Projetos existentes")

        if not selected_project:
            return None

        settings_file = Config.BASE_DIR / selected_project / "settings.json"

        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                existing_metadata = json.load(f)

            template_name = existing_metadata["titulo"].replace(" ", "_").capitalize()
            original_template_name = Config.BASE_DIR / selected_project / f"{template_name}.json"

            updated_metadata = self._collect_metadata(existing_metadata)

            new_template_name = updated_metadata["titulo"].replace(" ", "_").capitalize()
            updated_template_name = Config.BASE_DIR / selected_project / f"{new_template_name}.json"

            if os.path.exists(original_template_name):
                os.rename(original_template_name, updated_template_name)

            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(updated_metadata, f, ensure_ascii=False, indent=4)

            print(f"\n✓ Projeto {selected_project} atualizado com sucesso.")

            return selected_project, updated_metadata
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
        except json.JSONDecodeError:
            print("Erro ao ler arquivo de configuração.")
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")

        return None
