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
    return text

def parse_n_attribute(n_value):
    """Analyse l'attribut n avec un signe plus, retourne toutes les valeurs possibles de n.
       Si n_value est None, retourne une liste vide."""
    if n_value and '+' in n_value:
        return n_value.split('+')
    return [n_value] if n_value else []

def extract_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tLieu_objet\tLieu_loc\tTemps\tActeur\tPerc\tDoc\n")

        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyn_elements = {}
            lieu_obj_elements = {}
            lieu_loc_elements = {}
            tps_elements = {}
            act_elements = {}
            perc_elements = {}
            doc_elements = {}

            for dyn in phrase.findall('.//dyn'):
                dyn_n = dyn.get('n')
                if dyn_n:
                    dyn_elements[dyn_n] = html.unescape(get_element_text(dyn))
            
            for lieu in phrase.findall('.//lieu[@type="obj"]'):
                lieu_n = lieu.get('n')
                if lieu_n:
                    for n_value in parse_n_attribute(lieu_n):
                        lieu_obj_elements[n_value] = html.unescape(get_element_text(lieu))
            for lieu in phrase.findall('.//lieu[@type="loc"]'):
                lieu_n = lieu.get('n')
                if lieu_n:
                    for n_value in parse_n_attribute(lieu_n):
                        lieu_loc_elements[n_value] = html.unescape(get_element_text(lieu))

            for tps in phrase.findall('.//tps'):
                tps_n = tps.get('n')
                if tps_n:
                    tps_elements[tps_n] = html.unescape(get_element_text(tps))
            for act in phrase.findall('.//act'):
                act_n = act.get('n')
                if act_n:
                    act_elements[act_n] = html.unescape(get_element_text(act))
            for perc in phrase.findall('.//perc'):
                perc_n = perc.get('n')
                if perc_n:
                    perc_elements[perc_n] = html.unescape(get_element_text(perc))
            for doc in phrase.findall('.//doc'):
                doc_n = doc.get('n')
                if doc_n:
                    doc_elements[doc_n] = html.unescape(get_element_text(doc))

            # Assurer qu'au moins un dyn existe
            if dyn_elements:
                for n_value, dyn_text in dyn_elements.items():
                    lieu_obj_text = lieu_obj_elements.get(n_value, '')
                    lieu_loc_text = lieu_loc_elements.get(n_value, '')
                    tps_text = tps_elements.get(n_value, '')
                    act_text = act_elements.get(n_value, '')
                    perc_text = perc_elements.get(n_value, '')
                    doc_text = doc_elements.get(n_value, '')

                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{lieu_obj_text}\t{lieu_loc_text}\t{tps_text}\t{act_text}\t{perc_text}\t{doc_text}\n"
                    output_file.write(output_line)
            #else:
                # Si aucun dyn n'existe, écrire une ligne contenant seulement Numéro_Phrase et Nom_fichier
                #output_file.write(f"{nom_fichier}\t{i}\t\t\t\t\t\t\t\n")

input_file_path = '1959-MinistereConstructionNoteEtudeINSEE_20230710.xml'
output_file_path = 'test_simple.tsv'

extract_content_to_tsv(input_file_path, output_file_path)

print(f"Data extracted to: {output_file_path}")


