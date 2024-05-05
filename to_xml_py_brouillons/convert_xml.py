import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import re

# Fonction pour formater joliment la sortie XML
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def process_file(input_file, output_file):
    root = ET.Element('root')

    with open(input_file, 'r', encoding='utf-8') as file:
        prev_sentence = ""  # Utilisé pour stocker le contenu de la phrase précédente
        for line in file:
            line = line.strip()  # Supprimer les espaces au début et à la fin de la ligne
            line = re.sub(r'n=(\d+)', r'n="\1"', line)

            # Diviser les phrases en fonction de la ponctuation
            sentences = re.split(r'(?<=[.!?])\s+(?=.+\.)', line)
            for sentence in sentences:
                # Créer un nouvel élément phrase
                if sentence.strip():  # Ne traiter que les phrases non vides
                    sentence_elem = ET.SubElement(root, 'phrase')
                    sentence_elem.text = sentence.strip()

        # Formater joliment le XML et écrire dans un fichier
        xml_str = prettify(root)
        with open(output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_str)

def main():
    if len(sys.argv) != 3:
        print("Utilisation : python nom_du_script.py fichier_entree fichier_sortie")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)

if __name__ == "__main__":
    main()
