import re

def clean_broken_xml(xml_text):
    # Fix unescaped ampersands
    xml_text = re.sub(r"&(?!(amp|lt|gt|apos|quot);)", "&amp;", xml_text)

    # Remove malformed DOCTYPE
    xml_text = re.sub(r"<!DOCTYPE[^>]*>", "", xml_text)

    # Remove broken or invalid XML comments
    xml_text = re.sub(r"<\!--[^>]*-->", "", xml_text)

    # Fix TABLEATTRIBUTE and TRANSFORMFIELD that are missing closing tags
    xml_text = re.sub(r"(<TABLEATTRIBUTE[^>]+?)(?<!/)>", r"\1 />", xml_text)
    xml_text = re.sub(r"(<TRANSFORMFIELD[^>]+?)(?<!/)>", r"\1 />", xml_text)

    # Remove broken lines or leftovers
    xml_text = re.sub(r"=\s*\"[^\"]*\"[^>\n]*\n", "", xml_text)

    # Ensure proper root closing tag
    if not xml_text.strip().endswith("</POWERMART>"):
        xml_text += "\n</POWERMART>"

    return xml_text
