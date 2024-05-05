import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys

# Fonction pour formater joliment la sortie XML
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def process_file(input_file, output_file):
    root = ET.Element('root')

    with open(input_file, 'r', encoding='utf-8') as file:
        paragraph_elem = None  # Initialisation de la variable d'élément de paragraphe
        for line in file:
            line = line.strip()  # Supprimer les espaces au début et à la fin de la ligne
            if not line:
                # Ligne vide, indique le début d'un nouveau paragraphe
                paragraph_elem = None  # Réinitialisation de l'élément de paragraphe
                continue

            if paragraph_elem is None:
                # S'il n'y a pas d'élément de paragraphe actuel, en créer un nouveau
                paragraph_elem = ET.SubElement(root, 'Paragraphe')

            # Créer un élément de phrase pour la ligne (phrase) actuelle
            sentence_elem = ET.SubElement(paragraph_elem, 'Phrase')
            sentence_elem.text = line

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
