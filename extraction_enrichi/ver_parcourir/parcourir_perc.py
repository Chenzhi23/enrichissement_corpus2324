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
                        
                        # 构建n值到dyn的映射
                        dyn_map = {dyn.get('n'): dyn for dyn in dyns if dyn.get('n')}
                        default_dyn = [dyn for dyn in dyns if not dyn.get('n')]

                        for perc in percs:
                            perc_text = html.unescape(get_element_text(perc)).strip()
                            perc_type = perc.get('type', '').strip()
                            perc_pol = perc.get('pol', '').strip()
                            perc_n = perc.get('n')

                            if perc_text:  # 只处理有文本内容的perc元素
                                if perc_n:
                                    matched_dyns = [dyn_map.get(n) for n in perc_n.split('+') if n in dyn_map]
                                else:
                                    # 检查perc是否内嵌在某个dyn中
                                    parent_dyn = next((dyn for dyn in dyns if perc in list(dyn.iter())), None)
                                    matched_dyns = [parent_dyn] if parent_dyn else default_dyn

                                for dyn in matched_dyns:
                                    if dyn is not None:  # 确保dyn存在
                                        dyn_text = html.unescape(get_element_text(dyn)).strip()
                                        if dyn_text:  # 确保dyn有文本内容
                                            types = perc.get('type', '').split('+')  # Split multiple types
                                            for type_entry in types:  # Generate a row for each type
                                                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{perc_text}\t{type_entry}\t{perc_pol}\n"
                                                output_file.write(output_line)


# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_perc.tsv'

extract_perc_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")
