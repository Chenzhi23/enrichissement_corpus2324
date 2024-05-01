import os
import xml.etree.ElementTree as ET
import html


def get_element_text(element):
    """递归获取元素及其子元素的文本内容。"""
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text.strip()


def extract_act_content_to_tsv(file_path, output_file):
    """从XML文件中提取act内容，并将其保存到TSV文件中。"""
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_file, 'a', encoding='utf-8') as output_file:
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            acts = phrase.findall('.//act')

            act_elements = {}
            if acts:  # 如果存在<act>，则处理它
                for act in acts:
                    n = act.get('n')
                    if n:  # 检查n是否存在
                        n_values = n.split('+')
                        for n_value in n_values:
                            act_elements[n_value.strip()] = act
                    else:  # 如果没有n属性，则直接匹配dyn内容
                        act_elements[None] = act
            else:
                continue

            for dyn in dyns:
                n_value = dyn.get('n')
                dyn_text = html.unescape(get_element_text(dyn)).strip()
                act_text = ''
                act_type = ''

                act_element = act_elements.get(n_value.strip() if n_value else None)
                if act_element is not None:
                    act_text = html.unescape(get_element_text(act_element)).strip()
                    act_type = act_element.get('type', '').strip()

                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{act_text}\t{act_type}\n"
                output_file.write(output_line)


def process_xml_files_in_directory(directory_path, output_file_path):
    """处理文件夹中的所有XML文件，并将内容输出到TSV文件中。"""
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tType\n")

    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory_path, filename)
            extract_act_content_to_tsv(file_path, output_file_path)


# 请替换为你的文件夹路径
input_directory_path = 'your_directory_path'
output_file_path = 'all_files_act_contents.tsv'

process_xml_files_in_directory(input_directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
