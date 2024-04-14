import xml.etree.ElementTree as ET
import html
import os

# 新的辅助函数
def get_element_text(element):
    """递归获取元素及其子元素的文本内容"""
    text = element.text or ""
    for child in element:
        text += get_element_text(child)
        if child.tail:
            text += child.tail
    return text

def extract_content_to_tsv_detailed(file_path, output_path):
    # 从文件路径中提取文件名
    nom_fichier = os.path.basename(file_path)
    
    # 加载并解析XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 打开一个文件用于写入提取的数据，包括标题行
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 写入标题行，添加新的列名
        output_file.write("Numéro_Phrase\tNom_fichier\tdyn\taxe_temp\ttype\tabsolu\tSegment_Annoté\n")
        
        # 遍历每个<phrase>元素
        for i, phrase in enumerate(root.findall('.//phrase'), start=1):
            dyns = phrase.findall('.//dyn')
            tps_elements = {tps.get('n'): tps for tps in phrase.findall('.//tps')}
            
            # 如果没有dyn元素，仍然需要写入一行，但只有Numéro_Phrase和Nom_fichier
            if not dyns:
                output_file.write(f"{i}\t{nom_fichier}\t\t\t\t\t\n")
            else:
                # 对于每个dyn，查找匹配的tps
                for dyn in dyns:
                    n_value = dyn.get('n')
                    matching_tps = tps_elements.get(n_value)
                    
                    if matching_tps is not None:
                        tps_text = html.unescape(get_element_text(matching_tps))
                        absolu = matching_tps.get('absolu', '')
                        tps_axe_temp = matching_tps.get('axe_temp', '')
                        tps_type = matching_tps.get('type', '')
                    else:
                        tps_text = ''
                        absolu = ''
                        tps_axe_temp = ''
                        tps_type = ''
                    
                    dyn_text = html.unescape(get_element_text(dyn))
                    
                    # Segment_Annoté是tps元素的文本及其子元素的文本
                    segment_annoté = tps_text
                    
                    # 格式化并写入数据
                    output_line = f"{i}\t{nom_fichier}\t{dyn_text}\t{tps_axe_temp}\t{tps_type}\t{absolu}\t{segment_annoté}\n"
                    output_file.write(output_line)

# 更新文件路径
input_file_path_detailed = '1965-SDAURP_CE_Oct23.xml'  # 使用上传的文件路径
output_file_path_detailed = '1965-SDAURP_CE_Oct23.tsv'  # 更新输出文件的路径

# 调用函数
extract_content_to_tsv_detailed(input_file_path_detailed, output_file_path_detailed)

# 输出文件路径以便检查
print(f"Data extracted to: {output_file_path_detailed}")


