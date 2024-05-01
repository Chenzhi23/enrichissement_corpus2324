import xml.etree.ElementTree as ET
import html
import os

def get_element_text(element):
    """递归获取元素及其子元素的文本内容。"""
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text.strip()

def extract_doc_content_to_tsv(directory_path, output_path):
    """遍历指定文件夹中的所有XML文件，提取doc内容，并将其保存到一个TSV文件中。"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNumero_Phrase\tDynamique\tDoc_Text\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
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

# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_docs.tsv'

extract_doc_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
