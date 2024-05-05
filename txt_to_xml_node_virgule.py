import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import re

# Fonction pour formater la sortie XML
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Fonction pour traiter les correspondances
def process_match(match):
    group1 = match.group(1)
    group2 = match.group(2) if match.group(2) is not None else ""
    group3 = match.group(3) if match.group(3) is not None else ""
    # Si group2 existe, prendre le contenu après la virgule, sinon ne rien faire
    if group2:
        group2 = f'{group2[1:]}'  # Supprimer la virgule au début de group2, puis ajouter des guillemets
        # Si group3 existe, prendre le contenu après la virgule, sinon ne rien faire
        if group3:
            group3 = f'{group3[1:]}'
            return f'n="{group1}+{group2}+{group3}"'
        else:
            return f'n="{group1}+{group2}"'
    else:
        return f'n="{group1}"'


def process_file(input_file, output_file):
    root = ET.Element('root')

    with open(input_file, 'r', encoding='utf-8') as file:
        prev_sentence = ""  # Stocker le contenu de la phrase précédente
        for line in file:
            line = line.strip()  # Supprimer les espaces au début et à la fin de la ligne
            line = re.sub(r'n=(\d+)(,\d+)?(,\d+)?', process_match, line)

            # Diviser les phrases en fonction des signes de ponctuation
            sentences = re.split(r'(?<=[.!?])\s+(?=.+\.)', line)
            for sentence in sentences:
                # Créer un nouvel élément phrase
                if sentence.strip():  # Ne traiter que les phrases non vides
                    sentence_elem = ET.SubElement(root, 'phrase')
                    # Utiliser le texte directement comme texte de l'élément XML, sans échappement HTML
                    sentence_elem.text = sentence.strip()

        # Formater le XML et écrire dans un fichier
        xml_str = prettify(root)
        with open(output_file, 'w', encoding='utf-8') as output_file:
            # Remplacer &lt; et &gt; par < et > dans le texte
            output_file.write(xml_str.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\""))

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)

if __name__ == "__main__":
    main()



