from fpdf import FPDF
from fpdf.enums import XPos, YPos
from typing import Dict, List, Union, Tuple, Optional, Any


def paragraph(text: str, align: str = "J", **kwargs) -> Dict[str, Any]:
    """
    Creates a dictionary representing a paragraph configuration for some text
    with alignment, and additional optional key-value configurations.

    :param text: The content of the paragraph.
    :param align: The alignment of the text. Defaults to "J".
    :param kwargs: Additional key-value pairs for extended configuration.
    :return: A dictionary containing the paragraph configuration.
    :rtype: Dict[str, Any]
    """
    return {
        "type": "paragraph",
        "text": text,
        "align": align,
        **kwargs
    }


def subtitle(
        text: str,
        align: str = "L",
        size: int = 14,
        style: str = "B",
        **kwargs
) -> Dict[str, Any]:
    """
    Generates a dictionary representing a subtitle configuration for a document or
    interface. The dictionary includes details such as text content, alignment,
    font size, style, and any additional configuration passed through keyword
    arguments.

    :param text: The content of the subtitle.
    :param align: The alignment for the subtitle text. Defaults to "L".
    :param size: The font size for the subtitle. Defaults to 14.
    :param style: The font style for the subtitle. Defaults to "B".
    :param kwargs: Additional keyword arguments for extended configuration.

    :return: A dictionary containing the subtitle configuration with specified
             attributes and any additional settings provided.
    """
    return {
        "type": "subtitle",
        "text": text,
        "align": align,
        "font": {"size": size, "style": style},
        **kwargs
    }


def img(
        path: str,
        position: str = "center",
        width: int = 30,
        height: int = 20,
        text: str = "",
        **kwargs
) -> Dict[
    str, Any]:
    """
    Generates a dictionary representing an image element with given attributes.

    Summary:
    This function creates a dictionary representation for an image object, including
    properties such as file path, position, dimensions, optional text, and additional
    custom attributes. It is intended for usage in scenarios where structured image
    representation is required.

    :param path: File path to the image.
    :type path: str
    :param position: Position attribute for the image. Default value is "center".
    :type position: str
    :param width: Width of the image in pixels.
    :type width: int
    :param height: Height of the image in pixels.
    :type height: int
    :param text: Accompanying text or caption for the image. Defaults to an empty string.
    :type text: str
    :param kwargs: Additional arbitrary keyword arguments to include in the image representation.
    :type kwargs: dict
    :return: Dictionary containing the structured image attributes.
    :rtype: Dict[str, Any]
    """
    return {
        "type": "image",
        "path": path,
        "position": position,
        "width": width,
        "height": height,
        "text": text,
        **kwargs
    }


def img_right(
        path: str,
        text: str,
        width: int = 40,
        height: int = 30, **kwargs
) -> Dict[str, Any]:
    """
    Generates an image alignment configuration for positioning the image to the right.

    This function simplifies aligning an image on the right side of content. It constructs
    a configuration dictionary with alignment set to "right". The function relies on the
    lower-level `img` function for processing.

    :param path: The file path to the image.
    :type path: str
    :param text: The text or caption to accompany the image.
    :type text: str
    :param width: The width of the image. Defaults to 40.
    :type width: int
    :param height: The height of the image. Defaults to 30.
    :type height: int
    :param kwargs: Additional keyword arguments to be passed to the `img` function.
    :return: A dictionary representing the image configuration with specified alignment.
    :rtype: Dict[str, Any]
    """
    return img(path, "right", width, height, text, **kwargs)


def img_left(
        path: str,
        text: str,
        width: int = 40,
        height: int = 30,
        **kwargs
) -> Dict[str, Any]:
    """
    Adds an image with left alignment and specified properties like width, height, and
    additional styling. This function builds upon the `img` function, using the provided
    parameters and additional arguments to configure and return the image.

    :param path: Path to the image file.
    :type path: str
    :param text: Text description or label associated with the image.
    :type text: str
    :param width: Width of the image in pixels, default is 40.
    :type width: int
    :param height: Height of the image in pixels, default is 30.
    :type height: int
    :param kwargs: Additional keyword arguments to customize image properties.
    :type kwargs: dict
    :return: A dictionary containing the configuration of the styled image.
    :rtype: Dict[str, Any]
    """
    return img(path, "left", width, height, text, **kwargs)


def img_above(
        path: str,
        width: int = 60,
        height: int = 40,
        text: str = "",
        **kwargs
) -> Dict[str, Any]:
    """
    Generates an image element with its position specified as 'above'. This function
    serves as a convenient wrapper around the `img` function, allowing additional
    arguments and properties to be passed through `kwargs`. The user can specify
    the path to the image source, its dimensions, additional text, and any other
    custom settings.

    :param path: The file path or URL to the image.
    :param width: The width of the image in pixels. Defaults to 60.
    :param height: The height of the image in pixels. Defaults to 40.
    :param text: Optional text associated with the image element.
    :param kwargs: Additional keyword arguments for further customization.
    :return: A dictionary representing the image element and its attributes.
    """
    return img(path, "above", width, height, text, **kwargs)


def img_below(
        path: str,
        width: int = 60,
        height: int = 40,
        text: str = "",
        **kwargs
) -> Dict[str, Any]:
    """
    Generates a dictionary for creating an image with the specified parameters.
    The image is positioned 'below' and can be customized with the provided dimensions,
    optional text, and other additional keyword arguments.

    :param path: The file path to the image.
    :type path: str
    :param width: The width of the image in pixels. Default is 60.
    :type width: int, optional
    :param height: The height of the image in pixels. Default is 40.
    :type height: int, optional
    :param text: The optional text to overlay on the image. Default is an empty string.
    :type text: str, optional
    :param kwargs: Additional optional keyword arguments for image customization.
    :type kwargs: dict
    :return: A dictionary describing the image configuration.
    :rtype: dict
    """
    return img(path, "below", width, height, text, **kwargs)


class AcademicWork(FPDF):
    """
    Represents an academic work document generator following standards.

    This class is designed to help in creating and managing an academic work
    document. It provides methods for adding customized cover pages, back covers,
    summary pages, and other structural components of an academic work document.
    Users can leverage this class to generate standardized academic documents that
    adhere to specific stylistic and structural requirements.

    :ivar data: Contains the academic information such as the course, student
        name, title, city, year, discipline, and advisor.
    :type data: Dict[str, Any]
    :ivar logo_path: Path to the logo image to be inserted into the documents.
    :type logo_path: str
    :ivar mask_path: Optional path for a mask image that can be added to
        the document header.
    :type mask_path: Optional[str]
    :ivar sections: List of sections with their titles, page numbers, and
        corresponding anchors for linking within the document.
    :type sections: List[Tuple[str, int, str]]
    :ivar anchors: Dictionary mapping section anchors to their respective page
        numbers for cross-referencing.
    :type anchors: Dict[str, int]
    """

    def __init__(self, data: Dict[str, Any], logo_path: str, mask_path: Optional[str] = None):
        """
        Initialize the AcademicWork instance.

        Args:
            data: Dictionary containing course, student, title, city, year, discipline, and advisor information.
            logo_path: Path to the logo image.
            mask_path: Path to the mask image (optional).
        """
        super().__init__()
        self.data = data
        self.logo_path = logo_path
        self.mask_path = mask_path
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(25, 25, 25)
        self.sections: List[Tuple[str, int, str]] = []
        self.anchors: Dict[str, int] = {}

    def header(self) -> None:
        """
        Sets up the header for a document by placing an image over the defined area.

        If a valid `mask_path` is provided, the image is added to the document
        using the specified coordinates and dimensions.

        :param self: Reference to the current instance of the class.
        :return: None
        """
        if self.mask_path:
            self.image(self.mask_path, x=0, y=0, w=self.w, h=self.h)

    def footer(self) -> None:
        """
        Sets the footer of the document on each page. The footer includes the
        page number aligned to the center.

        The method adjusts the vertical position of the cursor to ensure the
        footer is always printed at the bottom of the page. It sets the font
        to 'Times' with a font size of 10 and renders the page number centered
        on the footer.

        :return: None
        """
        self.set_y(-15)
        self.set_font('Times', '', 10)
        self.cell(0, 10, f'{self.page_no()}', align='C')

    def add_cover(self) -> None:
        """
        Adds a cover page to the current document using predefined styles and content.

        This method generates a standardized cover page by adding elements such as a logo,
        institutional text, course information, student details, title, and other related details.
        It handles styling, alignment, and spacing to create a cohesive and professional layout.

        :param self: Refers to the current instance of the class.

        :raises Exception: An exception is raised if the image specified by ``self.logo_path`` cannot
            be loaded or displayed.

        :return: None
        """
        self.add_page()

        if self.logo_path:
            try:
                self.image(self.logo_path, x=(self.w - 40) / 2, y=20, w=40)
                self.ln(50)
            except:
                self.ln(20)
        else:
            self.ln(20)

        self.set_font('Times', 'B', 12)

        cover_texts = [
            "FUNDAÇÃO DE ASSISTÊNCIA E EDUCAÇÃO",
            "CENTRO UNIVERSITÁRIO ESPÍRITO-SANTENSE",
            f"CURSO DE GRADUAÇÃO EM {self.data['curso'].upper()}",
        ]

        for text in cover_texts:
            self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

        self.ln(30)
        self.cell(0, 8, self.data['aluno'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(30)
        self.multi_cell(0, 8, self.data['titulo'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(60)
        self.cell(0, 8, self.data['local'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)
        self.cell(0, 8, str(self.data['ano']), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def add_back_cover(self) -> None:
        """
        Adds a back cover page to the document with formatted information including the student's
        name, title, academic details, location, and year. This page is structured to follow
        academic formatting guidelines.

        The back cover includes:
        1. Student's name (in uppercase and centered).
        2. Title of the document (in uppercase and centered).
        3. Academic justification text, detailing the course, discipline, and advisor, formatted
           and aligned with justification alignment.
        4. Location and year information centered at the bottom.

        :param None
        :return: None
        """
        self.add_page()
        self.ln(40)

        self.set_font('Times', 'B', 12)
        self.cell(0, 8, self.data['aluno'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(30)
        self.multi_cell(0, 8, self.data['titulo'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(30)

        self.set_font('Times', '', 11)
        self.set_left_margin(100)
        justification_text = (
            f"Trabalho acadêmico do Curso de Graduação em {self.data['curso']} "
            f"apresentado ao Centro Universitário Espírito-santense como parte "
            f"das exigências da Disciplina {self.data['disciplina'].capitalize()},"
            f" sob orientação do(a) Professor(a) {self.data['orientador']}."
        )
        self.multi_cell(0, 6, justification_text, align='J')
        self.set_left_margin(25)
        self.ln(40)

        self.set_font('Times', 'B', 12)
        self.cell(0, 8, self.data['local'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)
        self.cell(0, 8, str(self.data['ano']), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def add_summary(self) -> None:
        """
        Generates and formats a summary section for a PDF document.

        The method creates a new page in the document, sets a title, and includes details
        about given sections, such as their titles, associated page numbers, and hyperlinks.
        Each section is styled with a determined number of dots for alignment.

        :raises ValueError: If section title or page number is invalid.
        """
        self.add_page()
        self.set_font('Times', 'B', 12)
        self.cell(0, 10, 'SUMÁRIO', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(20)
        self.set_font('Times', '', 12)

        for title, page, link_anchor in self.sections:
            necessary_dots = 60 - len(title) - len(str(page))
            dots = '.' * max(1, necessary_dots)
            self.set_text_color(0, 0, 0)
            self.cell(self.get_string_width(title), 8, title, link=self.anchors[link_anchor])
            self.cell(self.get_string_width(f" {dots} "), 8, f" {dots} ")
            self.cell(self.get_string_width(str(page)), 8, str(page), link=self.anchors[link_anchor])
            self.ln(10)

        self.set_text_color(0, 0, 0)

    def write_summary_on_page(self, summary_page: int) -> None:
        """
        Writes a summary to a specified page in the document.

        This method sets the document's current page to `summary_page`, formats the
        page with a 'SUMÁRIO' title, and lists each section title with its respective
        page number in a properly aligned manner. It adds a dotted line between the
        titles and the page numbers for better readability. After completing the
        summary, it restores the document's original page.

        :param summary_page: The page number where the summary will be written.
        :type summary_page: int
        """
        current_page = self.page_no()
        self.page = summary_page
        self.set_font('Times', 'B', 13)
        self.set_y(25)
        self.cell(0, 10, 'SUMÁRIO', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(20)
        self.set_font('Times', '', 12)

        for title, page, link_anchor in self.sections:
            title_width = self.get_string_width(title)
            page_width = self.get_string_width(str(page))
            total_width = self.w - self.l_margin - self.r_margin
            dot_width = total_width - title_width - page_width - 4

            self.set_text_color(0, 0, 0)
            self.cell(title_width, 8, title, link=self.anchors[link_anchor])
            self.cell(dot_width, 8, '.' * int(dot_width / self.get_string_width('.')))
            self.cell(page_width, 8, str(page), link=self.anchors[link_anchor], align='R')
            self.ln(10)

        self.set_text_color(0, 0, 0)
        self.page = current_page

    def _apply_font_and_color(
            self,
            item: Dict[str, Any],
            default_size: int = 12
    ) -> int:
        """
        Configure font and text color for a given item based on provided attributes or defaults.

        Args:
            item: Dictionary containing font and color configuration
            default_size: Default font size if not specified

        Returns:
            The font size being used
        """
        font = item.get("font", {})
        family = font.get("family", "Times")
        style = font.get("style") or ""
        size = font.get("size", default_size)
        self.set_font(family, style, size)

        color = item.get("color", (0, 0, 0))
        self.set_text_color(*color)
        return size

    def calculate_text_lines_and_height(
            self,
            text: str,
            width: float,
            line_height: float
    ) -> Tuple[List[str], float]:
        """
        Calculate text lines and their total height for rendering within a given width and line height.

        Args:
            text: The text content to be processed
            width: The maximum width available for each line of text
            line_height: The height of each line in the given text

        Returns:
            Tuple containing a list of text lines and total height
        """
        if not text:
            return [], 0

        lines = self.multi_cell(width, line_height, text, dry_run=True, output="LINES")
        total_height = len(lines) * line_height
        return lines, total_height

    def add_section(
            self,
            section_title: str,
            content: Union[str, List[Dict[str, Any]]] = ''
    ) -> None:
        """
        Add a new section with optional content to the document.

        Args:
            section_title: Title of the section
            content: Content of the section (string or list of content items)
        """
        self.add_page()
        link_anchor = f"section_{len(self.sections) + 1}"
        link_idx = self.add_link()
        self.anchors[link_anchor] = link_idx
        self.sections.append((section_title, self.page_no(), link_anchor))

        y = self.get_y()
        self.set_link(link_idx, page=self.page_no(), y=y)
        self.set_font('Times', 'B', 12)
        self.cell(0, 10, section_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

        if isinstance(content, str):
            self.set_font('Times', '', 12)
            self.multi_cell(0, 6, content, align='J')
            return

        page_width = self.w - self.l_margin - self.r_margin

        for item in content:
            item_type = item.get("type", "paragraph")

            if item_type == "paragraph":
                self._apply_font_and_color(item, default_size=12)
                line_h = item.get("line_height", 6)
                self.multi_cell(0, line_h, item.get("text", ""), align=item.get("align", "J"))
                self.ln(2)
                self.set_text_color(0, 0, 0)
                self.set_font('Times', '', 12)

            elif item_type == "subtitle":
                self._apply_font_and_color(item, default_size=14)
                line_h = item.get("line_height", 7)
                self.multi_cell(0, line_h, item.get("text", ""), align=item.get("align", "L"))
                self.ln(3)
                self.set_text_color(0, 0, 0)
                self.set_font('Times', '', 12)

            elif item_type == "image":
                pos = item.get("position", "right")
                img_w = item.get("width", 30)
                img_h = item.get("height", 20)
                img_path = item.get("path")
                text = item.get("text", "")
                margin_between = item.get("margin_between", 5)
                line_h = item.get("line_height", 6)

                if pos in ("left", "right") and text:
                    y_start = self.get_y()

                    if pos == "left":
                        img_x = self.l_margin
                        text_x = self.l_margin + img_w + margin_between
                        text_width = page_width - img_w - margin_between
                    else:
                        img_x = self.w - self.r_margin - img_w
                        text_x = self.l_margin
                        text_width = page_width - img_w - margin_between

                    self._apply_font_and_color(item, default_size=12)

                    try:
                        self.image(img_path, x=img_x, y=y_start, w=img_w, h=img_h)
                    except Exception:
                        pass

                    lines = self.multi_cell(text_width, line_h, text, dry_run=True, output="LINES")
                    max_lines_beside_image = int(img_h // line_h)

                    current_y = y_start
                    line_index = 0

                    while line_index < len(lines) and line_index < max_lines_beside_image:
                        line = lines[line_index]

                        if current_y > self.h - self.b_margin - line_h:
                            self.add_page()
                            current_y = self.get_y()
                            y_start = current_y

                            try:
                                self.image(img_path, x=img_x, y=current_y, w=img_w, h=img_h)
                            except Exception:
                                pass

                        self.set_xy(text_x, current_y)

                        if pos == "right":
                            align_for_cell = "L" if item.get("align", "J") == "J" else item.get("align", "L")
                            self.cell(text_width, line_h, line, align=align_for_cell)
                            current_y += line_h
                        else:
                            align_for_cell = "L" if item.get("align", "J") == "J" else item.get("align", "L")
                            self.cell(text_width, line_h, line, align=align_for_cell)
                            current_y += line_h
                        line_index += 1

                    if line_index < len(lines):
                        final_y = y_start + img_h + 2
                        self.set_xy(self.l_margin, final_y)
                        remaining_text = "\n".join(lines[line_index:])
                        if remaining_text.strip():
                            self.multi_cell(page_width, line_h, remaining_text, align=item.get("align", "J"))
                        final_y = self.get_y()
                    else:
                        final_y = y_start + img_h

                    self.set_xy(self.l_margin, final_y + 5)
                    self.set_text_color(0, 0, 0)
                    self.set_font('Times', '', 12)

                elif pos in ("left", "right") and not text:
                    img_x = self.l_margin if pos == "left" else (self.w - self.r_margin - img_w)
                    try:
                        self.image(img_path, x=img_x, y=self.get_y(), w=img_w, h=img_h)
                    except Exception:
                        pass
                    self.ln(img_h + 3)

                elif pos == "above":
                    img_x = self.l_margin + (page_width - img_w) / 2
                    try:
                        self.image(img_path, x=img_x, y=self.get_y(), w=img_w, h=img_h)
                    except Exception:
                        pass
                    self.ln(img_h + 3)

                    if text:
                        self._apply_font_and_color(item)
                        self.multi_cell(0, line_h, text, align=item.get("align", "J"))
                        self.set_text_color(0, 0, 0)
                        self.set_font('Times', '', 12)
                        self.ln(3)

                elif pos == "below":
                    if text:
                        self._apply_font_and_color(item)
                        self.multi_cell(0, line_h, text, align=item.get("align", "J"))
                        self.set_text_color(0, 0, 0)
                        self.set_font('Times', '', 12)
                        self.ln(2)

                    img_x = self.l_margin + (page_width - img_w) / 2
                    try:
                        self.image(img_path, x=img_x, y=self.get_y(), w=img_w, h=img_h)
                    except Exception:
                        pass
                    self.ln(img_h + 3)

                else:
                    img_x = self.l_margin + (page_width - img_w) / 2
                    try:
                        self.image(img_path, x=img_x, y=self.get_y(), w=img_w, h=img_h)
                    except Exception:
                        pass
                    self.ln(img_h + 3)

            elif item_type == "list":
                self.set_text_color(0, 0, 0)
                self.set_font('Times', '', 12)
                for reference in item.get("items", []):
                    self.multi_cell(0, 6, reference.replace("—", "-"), align="J")
                    self.ln(2)

        self.set_text_color(0, 0, 0)
        self.set_font('Times', '', 12)


class ContentBuilder:
    """
    A builder class to construct and manage a list of content elements such as paragraphs, subtitles, and images.

    The `ContentBuilder` class is designed to provide an easy-to-use interface for creating structured content
    by chaining method calls. Each method adds a specific type of content to the builder, with customizable
    attributes for formatting and layout. The user can retrieve the structured content or reset the builder
    state for creating new content.

    :ivar content: A list of dictionaries representing the content elements created by the builder.
                   Each dictionary contains information about the type of content (e.g., paragraph, subtitle, or image)
                   and its styling or positioning attributes.
    :type content: List[Dict[str, Any]]
    """

    def __init__(self):
        """
        Represents an initialization method for setting up an empty content list.

        The purpose of the constructor is to initialize the `content` attribute as an
        empty list. This list is meant to store dictionary objects where each dictionary
        is expected to have string keys and values of any type.

        :ivar content: A list intended to store dictionaries with string keys and values
            of any type. The attribute is initialized as an empty list during
            object instantiation.
        :vartype content: List[Dict[str, Any]]
        """
        self.content: List[Dict[str, Any]] = []

    def paragraph(
            self,
            text: str,
            align: str = "J",
            font_family: str = "Times",
            font_style: str = "",
            font_size: int = 12,
            color: Tuple[int, int, int] = (0, 0, 0),
            line_height: int = 6
    ) -> 'ContentBuilder':
        """
        Appends a paragraph configuration to the content list. This method allows detailed
        styling for a textual paragraph such as alignment, font properties, color, and
        line height. Each paragraph is stored as a dictionary with the necessary
        attributes to define its appearance and content.

        :param text: The textual content of the paragraph.
        :type text: str
        :param align: The alignment of the paragraph. Defaults to "J".
        :type align: str
        :param font_family: The font family of the paragraph text. Defaults to "Times".
        :type font_family: str
        :param font_style: The font style of the paragraph text. Defaults to an empty string.
        :type font_style: str
        :param font_size: The font size of the paragraph text. Defaults to 12.
        :type font_size: int
        :param color: The color of the paragraph text in RGB format. Defaults to (0, 0, 0).
        :type color: Tuple[int, int, int]
        :param line_height: The line height of the paragraph. Defaults to 6.
        :type line_height: int
        :return: Instance of the ContentBuilder for method chaining.
        :rtype: ContentBuilder
        """
        self.content.append({
            "type": "paragraph",
            "text": text,
            "align": align,
            "font": {"family": font_family, "style": font_style, "size": font_size},
            "color": color,
            "line_height": line_height
        })
        return self

    def subtitle(
            self,
            text: str,
            align: str = "L",
            font_family: str = "Times",
            font_style: str = "B",
            font_size: int = 14,
            color: Tuple[int, int, int] = (0, 0, 0),
            line_height: int = 7
    ) -> 'ContentBuilder':
        """
        Adds a subtitle to the content with specified text, formatting, and style options.

        :param text: Subtitle text to be added.
        :param align: Alignment of the subtitle text. Defaults to "L".
        :param font_family: Font family for the subtitle text. Defaults to "Times".
        :param font_style: Font style for the subtitle text. Defaults to "B".
        :param font_size: Font size for the subtitle text. Defaults to 14.
        :param color: RGB color value as a tuple for the subtitle text. Defaults to (0, 0, 0).
        :param line_height: Line height for the subtitle text. Defaults to 7.
        :return: The updated instance of ContentBuilder for method chaining.
        """
        self.content.append({
            "type": "subtitle",
            "text": text,
            "align": align,
            "font": {"family": font_family, "style": font_style, "size": font_size},
            "color": color,
            "line_height": line_height
        })
        return self

    def image(
            self,
            path: str,
            position: str = "center",
            width: int = 30,
            height: int = 20,
            text: str = "",
            margin_between: int = 5,
            align: str = "J",
            line_height: int = 6
    ) -> 'ContentBuilder':
        """
        Inserts an image into the content with specified attributes.

        This method allows adding an image with various customizable properties
        such as position, dimensions, accompanying text, margins, alignment,
        and line height.

        :param path: The file path of the image to be added.
        :param position: The alignment position of the image within the content,
            defaults to "center".
        :param width: The width of the image in units, defaults to 30.
        :param height: The height of the image in units, defaults to 20.
        :param text: Optional text to be displayed alongside the image,
            defaults to an empty string.
        :param margin_between: Space between the image and the text in units,
            defaults to 5.
        :param align: The text alignment relative to the image (e.g., "J"),
            defaults to "J".
        :param line_height: The height of the lines for the text in units,
            defaults to 6.
        :return: Returns the modified instance of ContentBuilder to allow
            method chaining.
        :rtype: ContentBuilder
        """
        self.content.append({
            "type": "image",
            "path": path,
            "position": position,
            "width": width,
            "height": height,
            "text": text,
            "margin_between": margin_between,
            "align": align,
            "line_height": line_height
        })
        return self

    def get_content(self) -> List[Dict[str, Any]]:
        """
        Retrieves the stored content.

        This method returns the content stored in the `content` attribute,
        which is a list of dictionaries containing various information.

        :return: A list of dictionaries containing the content data
        :rtype: List[Dict[str, Any]]
        """
        return self.content

    def clear(self) -> 'ContentBuilder':
        """
        Clears the content and resets it to an empty list.

        This method removes all existing elements in the content, leaving it
        empty, and allows chaining by returning the instance of the class.

        :return: The instance of the class itself to allow method chaining.
        :rtype: ContentBuilder
        """
        self.content = []
        return self


class Templates:
    """
    A collection of static methods providing various templates for combining
    images and text in structured layouts. These templates help in creating
    predefined sections with images and text for visual presentations or
    documentation purposes.
    """

    @staticmethod
    def image_with_text(
            image_path: str,
            text: str,
            position: str = "right",
            img_width: int = 40,
            img_height: int = 30
    ) -> Dict[str, Any]:
        """
        Generates an image with text overlay at a specified position and dimensions.

        This static method creates an image with text overlay based on the input
        parameters, such as image path, overlay text, position, and custom dimensions.
        It leverages the utility of the `img` function to process the inputs and
        assemble the image with desired text positioning and resizing.

        :param image_path: File path to the input image.
        :param text: Text to overlay on the image.
        :param position: Position of the text overlay on the image. Defaults to "right".
        :param img_width: Desired width of the output image. Defaults to 40.
        :param img_height: Desired height of the output image. Defaults to 30.
        :return: A dictionary containing the details of the generated image with text.
        """
        return img(image_path, position, img_width, img_height, text)

    @staticmethod
    def section_with_images(
            title: str,
            intro_text: str,
            image_path: str,
            demo_text: str
    ) -> List[Dict[str, Any]]:
        """
        Generates a structured layout section consisting of styled text and images in
        various configurations for display purposes including right-aligned, left-aligned,
        above, and below positions. It also demonstrates a paragraph between images for
        additional context or layout illustration.

        :param title: Title for the section content
        :param intro_text: Introductory text or description for the section
        :param image_path: File path or URL reference of the image to display
        :param demo_text: Description or demonstration text for the image
        :return: List of dictionaries representing various styled content blocks
            for the layout, including subtitles, paragraphs, and images.
        :rtype: List[Dict[str, Any]]
        """
        return [
            subtitle(title),
            paragraph(intro_text),
            img_right(image_path, demo_text),
            paragraph("Paragraph between images to demonstrate layout."),
            img_left(image_path, demo_text),
            img_above(image_path, text="Centered image above"),
            img_below(image_path, text="Text above this image")
        ]
