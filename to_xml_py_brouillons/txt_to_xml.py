import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys

# 用于美化XML输出的函数
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def process_file(input_file, output_file):
    # 创建XML的根元素
    root = ET.Element('root')

    # 读取并处理文件
    with open(input_file, 'r', encoding='utf-8') as file:
        paragraph_elem = None  # 初始化段落元素变量
        for line in file:
            line = line.strip()  # 删除行首尾的空格
            if not line:
                # 空行，表示一个新的段落开始
                paragraph_elem = None  # 重置段落元素
                continue

            if paragraph_elem is None:
                # 如果当前没有段落元素，创建一个新的
                paragraph_elem = ET.SubElement(root, 'Paragraphe')

            # 为当前行（句子）创建一个句子元素
            sentence_elem = ET.SubElement(paragraph_elem, 'Phrase')
            sentence_elem.text = line

    # 美化XML并写入文件
    xml_str = prettify(root)
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(xml_str)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)

if __name__ == "__main__":
    main()
