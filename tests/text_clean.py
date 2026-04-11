for reference in item.get("items", []):
    ref_text = reference.replace("—", "-")
    ref_text = ref_text.lstrip('0123456789. ')

    parts = ref_text.split('.')
    formatted_ref = ""

    if len(parts) >= 3:
        authors = parts[0] + '.'

        title_found = False
        for i, part in enumerate(parts[1:], 1):
            part_stripped = part.strip()
            if part_stripped and not part_stripped[0].isdigit() and len(part_stripped) > 3:
                if not title_found:
                    formatted_ref = authors + f' **{part_stripped}.**'
                    title_found = True
                else:
                    formatted_ref += part + '.'
            else:
                formatted_ref += part + '.'

        formatted_ref = formatted_ref.rstrip('.')
    else:
        formatted_ref = ref_text

    parts = text.split('**')
    x_start = self.get_x()

    for i, part in enumerate(parts):
        print(part)