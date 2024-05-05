import xml.etree.ElementTree as ET
import html
import os

def get_element_text(element):
    """Récupère récursivement le texte de l'élément et de ses éléments enfants."""
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text.strip()

def extract_dynamique_to_tsv(directory_path, output_path):
    """Parcourt tous les fichiers XML dans le dossier spécifié, extrait le contenu dyn et le sauvegarde dans un fichier TSV."""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNumero_Phrase\tSegment_Annoté\tAccompli\tNature\tTemps\tProces\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
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

directory_path = '../../corpus_xml/CE'
output_file_path = 'all_dyn.tsv'

extract_dynamique_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
