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

def parse_n_attribute(attribute):
    """将包含加号的n属性值解析为列表。"""
    if attribute:
        return attribute.split('+')
    return []

def extract_content_to_tsv(file_path, output_path):
    nom_fichier = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tDoc_Text\n")

        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            docs = phrase.findall('.//doc')

            # 为每个doc建立一个包含所有n值的映射
            doc_elements = {}
            for doc in docs:
                n_values = parse_n_attribute(doc.get('n'))
                doc_text = get_element_text(doc)
                for n_value in n_values:
                    if n_value:  # 确保n_value不是None
                        doc_elements[n_value.strip()] = doc_text

            for dyn in dyns:
                n_value = dyn.get('n')
                dyn_text = get_element_text(dyn)
                doc_text = ''

                if n_value:  # 确保n_value不是None
                    n_value = n_value.strip()  # 现在可以安全地调用strip
                    # 查找与dyn的n值匹配的doc文本
                    doc_text = doc_elements.get(n_value, '')

                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{doc_text}\n"
                output_file.write(output_line)

# 更新文件路径
input_file_path = 'output_file_2.xml'  # 更新为你的XML文件的实际路径
output_file_path = 'output_file_2_doc.tsv'  # 更新为你想要输出TSV文件的实际路径

extract_content_to_tsv(input_file_path, output_file_path)
print(f"Data extracted to: {output_file_path}")

