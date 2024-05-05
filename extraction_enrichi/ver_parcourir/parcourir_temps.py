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


def extract_tps_content_to_tsv(directory_path, output_path):
    """Parcourt tous les fichiers XML dans le dossier spécifié, extrait le contenu tps et le sauvegarde dans un fichier TSV."""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\taxe_temp\tabsolu\tType\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
                        dyns = phrase.findall('.//dyn')
                        tpss = phrase.findall('.//tps')

                        # Faire correspondre les dyns et les tps en fonction de l'attribut n ou de la relation interne
                        tps_map = {tps.get('n'): tps for tps in tpss if tps.get('n')}
                        default_tps = [tps for tps in tpss if not tps.get('n')]

                        for dyn in dyns:
                            dyn_text = html.unescape(get_element_text(dyn)).strip()
                            dyn_n = dyn.get('n')
                            matched_tpss = []

                            if dyn_n and dyn_n in tps_map:
                                matched_tpss.append(tps_map[dyn_n])
                            elif not dyn_n:
                                # Vérifier si le tps est imbriqué dans un dyn
                                matched_tpss = [tps for tps in default_tps if dyn in list(tps.iter())]
                                if not matched_tpss:
                                    matched_tpss = default_tps

                            for tps in matched_tpss:
                                tps_text = html.unescape(get_element_text(tps)).strip()
                                tps_axetemp = tps.get('axe_temp', '').strip()
                                tps_absolu = tps.get('absolu', '').strip()
                                tps_type = tps.get('type', '').strip()
                                if tps_text:
                                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{tps_text}\t{tps_axetemp}\t{tps_absolu}\t{tps_type}\n"
                                    output_file.write(output_line)


directory_path = '../../corpus_xml/CE'
output_file_path = 'all_tps.tsv'

extract_tps_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
