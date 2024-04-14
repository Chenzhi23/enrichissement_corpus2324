##把所有的东西都换成node的txt to xml
import re


# 读取文件内容的函数
def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 将内容转换为XML格式的函数
def convert_to_xml(content):
    # 根据标点符号分割内容成句子
    sentences = re.split(r'[.!?]\s+', content)

    # 为每个句子添加<phrase></phrase>标签
    xml_sentences = ['<phrase>{}</phrase>'.format(sentence) for sentence in sentences if sentence]

    # 连接所有句子
    return '<phrases>' + '\n'.join(xml_sentences) + '</phrases>'


# 将内容保存到新的XML文件的函数
def save_to_xml_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


# 主脚本
if __name__ == '__main__':
    input_filename = '2005-Reichen_20230710.txt'
    output_filename = 'outputNode_2005R.xml'

    # 读取原始文本文件的内容
    original_content = read_file_content(input_filename)

    # 将内容转换成XML格式
    xml_content = convert_to_xml(original_content)

    # 将XML内容保存到一个新文件
    save_to_xml_file(xml_content, output_filename)

    print(f'XML文件已保存为 {output_filename}')