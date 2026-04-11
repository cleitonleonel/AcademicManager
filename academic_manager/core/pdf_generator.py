from typing import Dict, Optional
from pathlib import Path
from academic_manager.config.settings import Config
from academic_manager.builder import AcademicWork


class PDFGenerator:
    """
    Provides utilities for generating academic project PDFs. This class is
    designed to handle the creation of PDF documents for academic works,
    incorporating metadata, templates, and additional formatting options
    such as logo and mask images. It provides customizable functionality
    to include sections, a cover page, a back cover, and a summary table
    in the PDF output.
    """

    @staticmethod
    def resolve_path(path: Path) -> Optional[str]:
        """
        Resolves the given file system path to its string representation if it exists.

        This method checks whether the specified path exists in the file system and,
        if it does, returns the string representation of the path in POSIX format.
        If the path does not exist, it returns None.

        Args:
            path (Path): The file system path to resolve.

        Returns:
            Optional[str]: The POSIX string representation of the path if it exists,
            or None otherwise.
        """
        return path.as_posix() if path.exists() else None

    def generate_pdf(
            self,
            project_name: str,
            metadata: Dict,
            template: Dict,
            options: Optional[Dict] = None
    ) -> bool:
        """
        Generates a PDF based on provided metadata and template.

        This static method creates and formats a PDF document using the contents
        provided in the metadata and template dictionaries. Additional resources
        such as logos or masks are also utilized if they exist in the expected
        directory layout for the project. After processing and formatting the
        PDF content (e.g. adding cover, sections, and back cover), the resulting
        file is saved to the disk.

        :param project_name: Name of the project, used for locating resources
                             and determining output file paths.
        :type project_name: str
        :param metadata: Dictionary containing metadata used to populate the
                         content of the PDF. This metadata is used to configure
                         various document properties and sections.
        :type metadata: Dict
        :param template: Dictionary defining the structure and content of the
                         PDF. It typically includes sections and their respective
                         blocks of text.
        :type template: Dict
        :return: A boolean indicating whether the PDF was successfully created
                 and saved without errors.
        :rtype: bool
        """
        try:
            project_path = Config.BASE_DIR / project_name
            filename = metadata["titulo"].replace(" ", "_").capitalize()

            mask_path, logo_path = None, None
            if not Config.IGNORE_MASKS or not Config.IGNORE_LOGO:
                logo_path = self.resolve_path(project_path / "sources" / "logo.png")
                mask_path = self.resolve_path(project_path / "sources" / "mask.png")

            pdf_path = project_path / f"{filename}.pdf"

            pdf = AcademicWork(metadata, logo_path, mask_path, options=options)

            pdf.add_cover()
            pdf.add_back_cover()
            pdf.add_page()

            summary_page = pdf.page_no()

            for section in template['sections']:
                name = section.get('name', '').upper()
                content = section.get('blocks', '')
                pdf.add_section(
                    name,
                    content=content,
                    ignore_img=Config.IGNORE_IMGS
                )

            pdf.write_summary_on_page(summary_page)
            pdf.output(str(pdf_path))

            print(f"✓ Trabalho gerado: {filename}.pdf")
            return True

        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            return False
