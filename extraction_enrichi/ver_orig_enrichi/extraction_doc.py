import xml.etree.ElementTree as ET
import html
import os

def get_element_text(element):
    """递归获取元素及其子元素的文本内容"""
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text

def extract_doc_content_to_tsv(file_path, output_path):
    # 从文件路径中提取文件名
    nom_fichier = os.path.basename(file_path)
    
    # 加载并解析XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 打开一个文件用于写入提取的数据，包括标题行
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 写入标题行
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\n")
        
        # 遍历每个<phrase>元素
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            doc_elements = {doc.get('n'): doc for doc in phrase.findall('.//doc')}
            
            # 如果没有dyn元素，仍然需要写入一行，但只有Numéro_Phrase和Nom_fichier
            if not dyns:
                output_file.write(f"{nom_fichier}\t{i}\t\t\n")
            else:
                # 对于每个dyn，查找匹配的doc
                for dyn in dyns:
                    n_value = dyn.get('n')
                    matching_doc = doc_elements.get(n_value)
                    
                    if matching_doc is not None:
                        doc_text = html.unescape(get_element_text(matching_doc))
                    else:
                        doc_text = ''
                    
                    dyn_text = html.unescape(get_element_text(dyn))
                    
                    # 格式化并写入数据
                    output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{doc_text}\n"
                    output_file.write(output_line)

# 更新文件路径
input_file_path = 'test_node_1965.xml'  # 请替换为您的输入文件路径
output_file_path = 'test_node_1965_doc.tsv'  # 请替换为您的输出文件路径

# 调用函数
extract_doc_content_to_tsv(input_file_path, output_file_path)

# 输出文件路径以便检查
print(f"Data extracted to: {output_file_path}")
