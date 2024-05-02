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
    return text.strip()


def extract_nouvelle_content_to_tsv(folder_path, output_path):
    # 打开一个文件用于写入提取的数据，包括标题行
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 写入标题行
        output_file.write("Nom_fichier\tNuméro_Phrase\tDynamique\tCause\tRes\tObj\n")

        # 遍历文件夹中的每个文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.xml'):
                file_path = os.path.join(folder_path, filename)
                # 从文件路径中提取文件名
                nom_fichier = os.path.basename(file_path)

                # 加载并解析XML文件
                tree = ET.parse(file_path)
                root = tree.getroot()

                # 遍历每个<phrase>元素
                for i, phrase in enumerate(root.findall('.//phrase'), start=1):
                    dyns = phrase.findall('.//dyn')
                    causes = phrase.findall('.//cause')
                    ress = phrase.findall('.//res')
                    objs = phrase.findall('.//obj')

                    # 如果 cause、res 和 obj 都为空，则跳过 dyn 的内容
                    if not any([causes, ress, objs]):
                        continue

                    cause_elements = {}
                    res_elements = {}
                    obj_elements = {}

                    if causes:
                        for cause in causes:
                            n = cause.get('n')
                            if n:
                                n_values = n.split('+')
                                for n_value in n_values:
                                    cause_elements[n_value.strip()] = cause
                            else:
                                cause_elements[None] = cause

                    if ress:
                        for res in ress:
                            n = res.get('n')
                            if n:
                                n_values = n.split('+')
                                for n_value in n_values:
                                    res_elements[n_value.strip()] = res
                            else:
                                res_elements[None] = res

                    if objs:
                        for obj in objs:
                            n = obj.get('n')
                            if n:
                                n_values = n.split('+')
                                for n_value in n_values:
                                    obj_elements[n_value.strip()] = obj
                            else:
                                obj_elements[None] = obj

                    for dyn in dyns:
                        n_value = dyn.get('n')
                        dyn_text = html.unescape(get_element_text(dyn)).strip()

                        cause_text = ''
                        res_text = ''
                        obj_text = ''

                        cause_element = cause_elements.get(n_value.strip() if n_value else None)
                        res_element = res_elements.get(n_value.strip() if n_value else None)
                        obj_element = obj_elements.get(n_value.strip() if n_value else None)

                        if not any([cause_element, res_element, obj_element]):
                            continue

                        if cause_element is not None:
                            cause_text = html.unescape(get_element_text(cause_element)).strip()
                        else:
                            cause_text = "none"

                        if res_element is not None:
                            res_text = html.unescape(get_element_text(res_element)).strip()
                        else:
                            res_text = "none"

                        if obj_element is not None:
                            obj_text = html.unescape(get_element_text(obj_element)).strip()
                        else:
                            obj_text = "none"

                        # 如果 cause、res 和 obj 内容都为空，则跳过写入
                        # if not any([cause_text, res_text, obj_text]):
                        #     continue


                        # 格式化并写入数据
                        output_line = f"{nom_fichier}\t{i}\t{dyn_text}\t{cause_text}\t{res_text}\t{obj_text}\n"
                        output_file.write(output_line)


# 更新文件夹路径和输出文件路径
input_folder_path = '../../corpus_xml/CE'  # 请替换为您的输入文件夹路径
output_file_path = 'all_nouvelle.tsv'  # 请替换为您的输出文件路径

# 调用函数
extract_nouvelle_content_to_tsv(input_folder_path, output_file_path)

# 输出文件路径以便检查
print(f"Data extracted to: {output_file_path}")
