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

def extract_dynamique_to_tsv(file_path, output_path):
    # 从文件路径中提取文件名
    nom_fichier = os.path.basename(file_path)
    
    # 加载并解析XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 打开一个文件用于写入提取的数据，包括标题行
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 写入标题行，添加新的列名
        output_file.write("Nom_fichier\tNumero_Phrase\tSegment_Annoté\tAccompli\tNature\tTemps\tProces\n")


        # 遍历每个<phrase>元素
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            # 查找当前phrase下的所有dyn元素
            dyns = phrase.findall('.//dyn')
            if not dyns:
                # 如果没有dyn元素，仍然需要写入一行，但只有Numéro_Phrase和Nom_fichier
                output_file.write(f"{nom_fichier}\t{i}\t\t\t\t\t\n")
            else:
                # 对于每个dyn，写入相应的数据行
                for dyn in dyns:
                    # 获取dyn元素的相关信息
                    dyn_text = html.unescape(get_element_text(dyn))
                    attrib_accompli = dyn.get('accompli', '')
                    attrib_nature = dyn.get('nature', '')
                    attrib_proces = dyn.get('proces', '')
                    attrib_temps = dyn.get('temps', '')
                    
                    # 获取<dyn>和</dyn>之间的文本内容作为Segment_Annoté
                    segment_annoté = get_element_text(dyn).strip()
                    
                    # 写入数据到文件
                    output_line = f"{nom_fichier}\t{i}\t{segment_annoté}\t{attrib_accompli}\t{attrib_nature}\t{attrib_temps}\t{attrib_proces}\n"
                    output_file.write(output_line)

# 更新文件路径
input_file_path_detailed = 'test_node_2005SCE.xml'  # 使用上传的文件路径
output_file_path_detailed = 'test_node_2005SCE_dynamique.tsv'  # 更新输出文件的路径

# 调用函数
extract_dynamique_to_tsv(input_file_path_detailed, output_file_path_detailed)

# 输出文件路径以便检查
print(f"Data extracted to: {output_file_path_detailed}")
