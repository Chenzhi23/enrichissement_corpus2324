import pymysql
import csv
import argparse


def connect_database():
    try:
        conn = pymysql.Connect(
            host='127.0.0.1',
            user='root',
            port=3306,
            password='Ct010327',
            database='projet_enrichissement',
            charset='utf8'
        )
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("not connected")


def main(csv_path, nom_table):
    conn, cursor=connect_database()
    with open(csv_path, encoding='utf8') as file:
        table = csv.reader(file, delimiter='\t')
        next(table)
        id = 1
        for ligne in table:
            for index, element in enumerate(ligne):
                if element.isdigit():
                    ligne[index] = int(element)
            ligne = tuple(ligne)

            num_colonne = len(ligne)
            sql = f"INSERT INTO {nom_table} " + f"VALUES({id}," + "%s,"*(num_colonne-1) +"%s)"
            id += 1
            cursor.execute(sql, ligne)
            conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--csv_path', type=str, help='the csv file path to be input')
    parser.add_argument('-t', '--table_name', type=str, help='which table you want to insert data from csv')

    args = parser.parse_args()

    main(args.csv_path, args.table_name)
