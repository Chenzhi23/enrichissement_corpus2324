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

def extract_dynamique_to_tsv(directory_path, output_path):
    """遍历文件夹中的所有XML文件，提取其中的动态信息，然后将其保存到TSV文件中。"""
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

# 文件夹路径和输出文件路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_dyn.tsv'

extract_dynamique_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
