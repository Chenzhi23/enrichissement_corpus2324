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


def extract_lieu_content_to_tsv(directory_path, output_path):
    """遍历指定文件夹中的所有XML文件，提取act内容，并将其保存到一个TSV文件中。"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tSegment_Annoté\tType\n")

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    nom_fichier = os.path.basename(file_path)
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    for i, phrase in enumerate(root_element.findall('.//phrase'), start=1):
                        dyns = phrase.findall('.//dyn')
                        lieux = phrase.findall('.//lieu')

                        # 将dyn和act根据n属性或内部关系进行匹配
                        dyn_map = {dyn.get('n'): dyn for dyn in dyns if dyn.get('n')}
                        default_dyn = [dyn for dyn in dyns if not dyn.get('n')]

                        for lieu in lieux:
                            lieu_text = html.unescape(get_element_text(lieu)).strip()
                            lieu_type = lieu.get('type', '').strip()
                            lieu_n = lieu.get('n')

                            if lieu_n:
                                matched_dyns = [dyn_map[n] for n in lieu_n.split('+') if n in dyn_map]
                            else:
                                # 检查lieu是否内嵌在某个dyn中
                                parent_dyn = next((dyn for dyn in dyns if lieu in list(dyn.iter())), None)
                                if parent_dyn:
                                    matched_dyns = [parent_dyn]
                                else:
                                    matched_dyns = default_dyn  # 如果lieu没有n属性且不是内嵌，关联到所有没有n的dyn

                            for dyn in matched_dyns:
                                dyn_text = html.unescape(get_element_text(dyn)).strip()
                                output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{lieu_text}\t{lieu_type}\n"
                                output_file.write(output_line)


# 请替换为你的文件夹路径
directory_path = '../../corpus_xml/CE'
output_file_path = 'all_lieux.tsv'

extract_lieu_content_to_tsv(directory_path, output_file_path)
print(f"Data extracted to: {output_file_path}")

