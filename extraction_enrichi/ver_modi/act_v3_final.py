import xml.etree.ElementTree as ET
import html
import os

def get_element_text(element):
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text.strip()

def extract_act_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tType\n")
        
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            acts = phrase.findall('.//act')

            act_elements = {}
            if acts:
                for act in acts:
                    n = act.get('n')

                    if n:
                        n_values = n.split('+')
                        for n_value in n_values:
                            act_elements[n_value.strip()] = act
                    else:
                        act_elements[None] = act
            else:
                continue
            
            for dyn in dyns:
                n_value = dyn.get('n')
                dyn_text = html.unescape(get_element_text(dyn)).strip()
                act_text = ''
                act_type = ''

                act_element = act_elements.get(n_value.strip() if n_value else None)
                if act_element is not None:
                    act_text = html.unescape(get_element_text(act_element)).strip()
                    act_type = act_element.get('type', '').strip()

                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{act_text}\t{act_type}\n"
                output_file.write(output_line)

input_file_path = '../test.xml'
output_file_path = 'test_act.tsv'

extract_act_content_to_tsv(input_file_path, output_file_path)
print(f"Data extracted to: {output_file_path}")






