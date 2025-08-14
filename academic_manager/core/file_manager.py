from typing import List
from academic_manager.config.settings import Config


class FileManager:
    """
    Manages file operations such as directory creation and file listing.

    This class provides static methods to handle common file management tasks,
    including ensuring the existence of necessary directories, listing projects,
    assignments, and attachments related to specified projects.

    """

    @staticmethod
    def ensure_directories_exist():
        """
        Ensures the required directories exist by creating them if they do not already exist.

        This method checks for the existence of specific directories that are
        essential for the application's proper operation. If any of these directories
        are missing, they will be created. The directories are created with the
        default permissions.

        :raises FileExistsError: If a directory with the same name exists but it is not
            a directory.
        """
        Config.BASE_DIR.mkdir(exist_ok=True)
        Config.ASSIGNMENTS_DIR.mkdir(exist_ok=True)

    @staticmethod
    def list_projects() -> List[str]:
        """
        Lists all project directories excluding the 'assignments' directory if present.

        This method identifies subdirectories within the base directory defined in the
        configuration, excluding the directory named "assignments." It returns a
        sorted list of names of the identified directories. If the base directory does
        not exist, it returns an empty list.

        :rtype: List[str]
        :return: A sorted list of project directory names excluding "assignments".
        """
        if not Config.BASE_DIR.exists():
            return []

        return sorted([
            d.name for d in Config.BASE_DIR.iterdir()
            if d.is_dir() and d.name != "assignments"
        ])

    @staticmethod
    def list_assignments() -> List[str]:
        """
        Lists all assignment files in the configured assignments directory.

        This method checks if the assignments directory exists. If it does not
        exist, an empty list is returned. Otherwise, it iterates over the contents
        of the directory, filters for files, and returns a sorted list of their
        names.

        :return: A sorted list of file names in the assignments directory. If the
                 directory does not exist, it returns an empty list.
        :rtype: List[str]
        """
        if not Config.ASSIGNMENTS_DIR.exists():
            return []

        return sorted([
            f.name for f in Config.ASSIGNMENTS_DIR.iterdir()
            if f.is_file()
        ])

    @staticmethod
    def list_attachments(project_name: str) -> List[str]:
        """
        Lists all attachment filenames within the attachments directory of a specified project.

        The function identifies the attachments folder for the given project name and returns
        a sorted list of filenames present in that folder. If the directory does not exist,
        an empty list is returned.

        :param project_name: The name of the project for which attachment filenames are listed.
        :type project_name: str
        :return: A sorted list of attachment filenames in the project's attachments folder.
                 Returns an empty list if the folder does not exist.
        :rtype: List[str]
        """
        attachments_dir = Config.BASE_DIR / project_name / "attachments"
        if not attachments_dir.exists():
            return []

        return sorted([
            f.name for f in attachments_dir.iterdir()
            if f.is_file()
        ])
