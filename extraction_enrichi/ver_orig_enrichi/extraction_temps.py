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

def extract_content_to_tsv_detailed(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Numéro_Phrase\tNom_fichier\tdyn\taxe_temp\ttype\tabsolu\tSegment_Annoté\n")
        
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            tps_elements = {tps.get('n'): tps for tps in phrase.findall('.//tps')}
            
            if not dyns:
                output_file.write(f"{i}\t{nom_fichier}\t\t\t\t\t\n")
            else:
                for dyn in dyns:
                    n_value = dyn.get('n')
                    matching_tps = tps_elements.get(n_value)
                    
                    if matching_tps is not None:
                        tps_text = html.unescape(get_element_text(matching_tps))
                        absolu = matching_tps.get('absolu', '')
                        tps_axe_temp = matching_tps.get('axe_temp', '')
                        tps_type = matching_tps.get('type', '')
                    else:
                        tps_text = ''
                        absolu = ''
                        tps_axe_temp = ''
                        tps_type = ''
                    
                    dyn_text = html.unescape(get_element_text(dyn))
                    
                    segment_annoté = tps_text
                    
                    output_line = f"{i}\t{nom_fichier}\t{dyn_text}\t{tps_axe_temp}\t{tps_type}\t{absolu}\t{segment_annoté}\n"
                    output_file.write(output_line)

input_file_path_detailed = '1965-SDAURP_CE_Oct23.xml'
output_file_path_detailed = '1965-SDAURP_CE_Oct23.tsv'

extract_content_to_tsv_detailed(input_file_path_detailed, output_file_path_detailed)

print(f"Data extracted to: {output_file_path_detailed}")


