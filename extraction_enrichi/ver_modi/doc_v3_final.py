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

def extract_doc_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNumero_Phrase\tDynamique\tDoc_Text\n")

        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            docs = phrase.findall('.//doc')

            doc_elements = {}
            if docs:
                for doc in docs:
                    n = doc.get('n')
                    if n:
                        n_values = n.split('+')
                        for n_value in n_values:
                            doc_elements[n_value.strip()] = doc
                    else:
                        doc_elements[None] = doc
            else:
                continue

            for dyn in dyns:
                n_value = dyn.get('n')
                dyn_text = html.unescape(get_element_text(dyn)).strip()
                doc_text = ''

                doc_element = doc_elements.get(n_value.strip() if n_value else None)
                if doc_element is not None:
                    doc_text = html.unescape(get_element_text(doc_element)).strip()

                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{doc_text}\n"
                output_file.write(output_line)

input_file_path = 'test.xml'
output_file_path = 'test_doc.tsv'

extract_doc_content_to_tsv(input_file_path, output_file_path)
print(f"Data extracted to: {output_file_path}")




