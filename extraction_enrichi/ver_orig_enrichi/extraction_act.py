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

def extract_act_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tType\n")
        
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            act_elements = {act.get('n'): act for act in phrase.findall('.//act')}
            
            if not dyns:
                output_file.write(f"{nom_fichier}\t{i}\t\t\t\n")
            else:
                for dyn in dyns:
                    n_value = dyn.get('n')
                    matching_act = act_elements.get(n_value)
                    
                    if matching_act is not None:
                        act_text = html.unescape(get_element_text(matching_act))
                        act_type = matching_act.get('type', '')
                    else:
                        act_text = ''
                        act_type = ''
                    
                    dyn_text = html.unescape(get_element_text(dyn))
                    
                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{act_text}\t{act_type}\n"
                    output_file.write(output_line)

input_file_path = 'test_node_1965.xml'
output_file_path = 'test_node_1965_act.tsv'

extract_act_content_to_tsv(input_file_path, output_file_path)

print(f"Data extracted to: {output_file_path}")


