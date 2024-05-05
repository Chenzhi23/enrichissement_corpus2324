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

def extract_lieu_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tLieu_Type\n")
        
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            lieu_elements = {lieu.get('n'): lieu for lieu in phrase.findall('.//lieu')}
            
            if not dyns:
                output_file.write(f"{nom_fichier}\t{i}\t\t\t\n")
            else:
                for dyn in dyns:
                    n_value = dyn.get('n')
                    matching_lieu = lieu_elements.get(n_value)
                    
                    if matching_lieu is not None:
                        lieu_text = html.unescape(get_element_text(matching_lieu))
                        lieu_type = matching_lieu.get('type', '')
                    else:
                        lieu_text = ''
                        lieu_type = ''
                    
                    dyn_text = html.unescape(get_element_text(dyn))
                    
                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{lieu_text}\t{lieu_type}\n"
                    output_file.write(output_line)

input_file_path = 'test_node_1965.xml'
output_file_path = 'test_node_1965_lieu.tsv'

extract_lieu_content_to_tsv(input_file_path, output_file_path)

print(f"Data extracted to: {output_file_path}")

