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

def extract_dynamique_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNumero_Phrase\tSegment_Annoté\tAccompli\tNature\tTemps\tProces\n")


        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            for dyn in dyns:
                dyn_text = html.unescape(get_element_text(dyn))
                attrib_accompli = dyn.get('accompli', '')
                attrib_nature = dyn.get('nature', '')
                attrib_proces = dyn.get('proces', '')
                attrib_temps = dyn.get('temps', '')

                segment_annoté = get_element_text(dyn).strip()

                output_line = f"{nom_fichier}\t{i}\t{segment_annoté}\t{attrib_accompli}\t{attrib_nature}\t{attrib_temps}\t{attrib_proces}\n"
                output_file.write(output_line)

input_file_path_detailed = '../../corpus_xml/CE/2003-Corajoud_CE_Oct23.xml'
output_file_path_detailed = 'test_dyn.tsv'

extract_dynamique_to_tsv(input_file_path_detailed, output_file_path_detailed)

print(f"Data extracted to: {output_file_path_detailed}")
