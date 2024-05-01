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

def extract_tps_content_to_tsv(directory_path, output_path):
    """遍历指定文件夹中的所有XML文件，提取tps内容，并将其保存到一个TSV文件中。"""
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

                        tps_elements = {}
                        if tpss:  # 处理<tps>元素
                            for tps in tpss:
                                n = tps.get('n')
                                if n:  # 检查n属性
                                    n_values = n.split('+')
                                    for n_value in n_values:
                                        tps_elements[n_value.strip()] = tps
                                else:  # 没有n属性的情况
                                    tps_elements[None] = tps
                        else:
                            continue

                        for dyn in dyns:
                            n_value = dyn.get('n')
                            dyn_text = html.unescape(get_element_text(dyn)).strip()
                            tps_text = ''
                            tps_axetemp = ''
                            tps_absolu = ''
                            tps_type = ''

                            tps_element = tps_elements.get(n_value.strip() if n_value else None)
                            if tps_element is not None:
                                tps_text = html.unescape(get_element_text(tps_element)).strip()
                                tps_axetemp = tps_element.get('axe_temp', '').strip()
                                tps_absolu = tps_element.get('absolu', '').strip()
                                tps_type = tps_element.get('type', '').strip()

                            output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{tps_text}\t{tps_axetemp}\t{tps_absolu}\t{tps_type}\n"
                            output_file.write(output_line)

# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_tps.tsv'

extract_tps_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
