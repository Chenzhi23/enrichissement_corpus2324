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

def extract_perc_content_to_tsv(directory_path, output_path):
    """遍历指定文件夹中的所有XML文件，提取perc内容，并将其保存到一个TSV文件中。"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tType\tPol\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
                        dyns = phrase.findall('.//dyn')
                        percs = phrase.findall('.//perc')

                        perc_elements = {}
                        if percs:  # 处理<perc>元素
                            for perc in percs:
                                n = perc.get('n')
                                if n:  # 如果有n属性
                                    n_values = n.split('+')
                                    for n_value in n_values:
                                        perc_elements[n_value.strip()] = perc
                                else:  # 没有n属性，与dyn匹配
                                    perc_elements[None] = perc
                        else:
                            continue

                        for dyn in dyns:
                            n_value = dyn.get('n')
                            dyn_text = html.unescape(get_element_text(dyn)).strip()
                            perc_text = ''
                            perc_type = ''
                            perc_pol = ''

                            perc_element = perc_elements.get(n_value.strip() if n_value else None)
                            if perc_element is not None:
                                perc_text = html.unescape(get_element_text(perc_element)).strip()
                                perc_type = perc_element.get('type', '').strip()
                                perc_pol = perc_element.get('pol', '').strip()

                            output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{perc_text}\t{perc_type}\t{perc_pol}\n"
                            output_file.write(output_line)

# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_perc.tsv'

extract_perc_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
