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

def extract_tps_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\taxe_temp\tabsolu\tType\n")
        
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            tpss = phrase.findall('.//tps')

            tps_elements = {}
            if tpss:
                for tps in tpss:
                    n = tps.get('n')
                    if n:
                        n_values = n.split('+')
                        for n_value in n_values:
                            tps_elements[n_value.strip()] = tps
                    else:
                        tps_elements[None] = tps
            else:
                continue
            
            for dyn in dyns:
                n_value = dyn.get('n')
                dyn_text = html.unescape(get_element_text(dyn)).strip()
                tps_text = ''
                tps_axetemp = ''
                tps_absolu = ''
                tps_type = ''


                tps_element = tps_elements.get(n_value.strip() if n_value else None)
                if tps_element is not None:
                    tps_text = html.unescape(get_element_text(tps_element)).strip()
                    tps_axetemp = tps_element.get('axe_temp', '').strip()
                    tps_absolu = tps_element.get('absolu', '').strip()
                    tps_type = tps_element.get('type', '').strip()

                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{tps_text}\t{tps_axetemp}\t{tps_absolu}\t{tps_type}\n"
                output_file.write(output_line)

input_file_path = 'test.xml'
output_file_path = 'test_tps.tsv'

extract_tps_content_to_tsv(input_file_path, output_file_path)
print(f"Data extracted to: {output_file_path}")






