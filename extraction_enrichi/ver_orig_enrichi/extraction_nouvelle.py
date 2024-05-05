import xml.etree.ElementTree as ET
import html
import os

def get_element_text(element):
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text

def extract_new_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tCause\tRes\tObj\n")

        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            cause_text = html.unescape(get_element_text(phrase.find('.//cause'))) if phrase.find(
                './/cause') is not None else ''
            res_text = html.unescape(get_element_text(phrase.find('.//res'))) if phrase.find(
                './/res') is not None else ''
            obj_text = html.unescape(get_element_text(phrase.find('.//obj'))) if phrase.find(
                './/obj') is not None else ''

            if not any([cause_text, res_text, obj_text]):
                continue

            dyns = phrase.findall('.//dyn')
            for dyn in dyns:
                    dyn_text = html.unescape(get_element_text(dyn))

                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{cause_text}\t{res_text}\t{obj_text}\n"
                    output_file.write(output_line)


input_file_path = 'test.xml'
output_file_path = 'test_nouvelle_output.tsv'

extract_new_content_to_tsv(input_file_path, output_file_path)

print(f"Data extracted to: {output_file_path}")
