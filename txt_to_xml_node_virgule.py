import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import re

# 用于美化XML输出的函数
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def process_match(match):
    group1 = match.group(1)
    group2 = match.group(2) if match.group(2) is not None else ""
    group3 = match.group(3) if match.group(3) is not None else ""
    # 如果group2存在，则取逗号后的内容，否则不处理
    if group2:
        group2 = f'{group2[1:]}'  # 去掉group2开头的逗号，然后添加引号
        # 如果group3存在，则取逗号后的内容，否则不处理
        if group3:
            group3 = f'{group3[1:]}'
            return f'n="{group1}+{group2}+{group3}"'
        else:
            return f'n="{group1}+{group2}"'
    else:
        return f'n="{group1}"'


def process_file(input_file, output_file):
    # 创建XML的根元素
    root = ET.Element('root')

    # 读取并处理文件
    with open(input_file, 'r', encoding='utf-8') as file:
        prev_sentence = ""  # 用于存储前一个句子的内容
        for line in file:
            line = line.strip()  # 删除行首尾的空格
            line = re.sub(r'n=(\d+)(,\d+)?(,\d+)?', process_match, line)

            # 根据标点符号分割句子
            sentences = re.split(r'(?<=[.!?])\s+(?=.+\.)', line)
            for sentence in sentences:
                # 创建一个新的句子元素
                if sentence.strip():  # 只处理非空句子
                    sentence_elem = ET.SubElement(root, 'phrase')
                    # 将文本直接作为XML元素的文本，而不进行HTML转义
                    sentence_elem.text = sentence.strip()

        # 美化XML并写入文件
        xml_str = prettify(root)
        with open(output_file, 'w', encoding='utf-8') as output_file:
            # 将文本中的 &lt; 和 &gt; 替换为 < 和 >
            output_file.write(xml_str.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\""))

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)

if __name__ == "__main__":
    main()



