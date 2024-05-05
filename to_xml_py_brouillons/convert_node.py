import re


# Fonction pour lire le contenu du fichier
def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# Fonction pour convertir le contenu en format XML
def convert_to_xml(content):
    # Diviser le contenu en phrases en fonction de la ponctuation
    sentences = re.split(r'[.!?]\s+', content)

    # Ajouter des balises <phrase></phrase> à chaque phrase
    xml_sentences = ['<phrase>{}</phrase>'.format(sentence) for sentence in sentences if sentence]

    # Concaténer toutes les phrases
    return '<phrases>' + '\n'.join(xml_sentences) + '</phrases>'


# Fonction pour enregistrer le contenu dans un nouveau fichier XML
def save_to_xml_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == '__main__':
    input_filename = '2005-Reichen_20230710.txt'
    output_filename = 'outputNode_2005R.xml'

    # Lire le contenu du fichier texte original
    original_content = read_file_content(input_filename)

    # Convertir le contenu en format XML
    xml_content = convert_to_xml(original_content)

    # Enregistrer le contenu XML dans un nouveau fichier
    save_to_xml_file(xml_content, output_filename)

    print(f'Le fichier XML a été enregistré sous le nom de {output_filename}')
