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

def parse_n_attribute(n_value):
    """解析具有加号的n属性，返回所有可能的n值。
       如果n_value为None，则返回一个空列表。"""
    if n_value and '+' in n_value:
        return n_value.split('+')
    return [n_value] if n_value else []

def extract_content_to_tsv(directory_path, output_path):
    """遍历文件夹中的所有XML文件，提取内容，并将其保存到一个TSV文件中。"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tLieu_objet\tLieu_loc\tTemps\tActeur\tPerc\tDoc\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
                        dyn_elements = {}
                        lieu_obj_elements = {}
                        lieu_loc_elements = {}
                        tps_elements = {}
                        act_elements = {}
                        perc_elements = {}
                        doc_elements = {}

                        for element_type, elements_dict, xpath, attribute in [
                            ('dyn', dyn_elements, './/dyn', None),
                            ('lieu', lieu_obj_elements, './/lieu[@type="obj"]', 'n'),
                            ('lieu', lieu_loc_elements, './/lieu[@type="loc"]', 'n'),
                            ('tps', tps_elements, './/tps', 'n'),
                            ('act', act_elements, './/act', 'n'),
                            ('perc', perc_elements, './/perc', 'n'),
                            ('doc', doc_elements, './/doc', 'n')]:
                            for element in phrase.findall(xpath):
                                n = element.get(attribute) if attribute else None
                                if n:
                                    for n_value in parse_n_attribute(n):
                                        elements_dict[n_value] = html.unescape(get_element_text(element))
                                else:
                                    elements_dict[None] = html.unescape(get_element_text(element))

                        # 输出数据
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

# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/simple'
output_file_path = 'all_simple.tsv'

extract_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
