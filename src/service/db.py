import mysql.connector as connector



def insert_into_database(tableName,dic):
    conn = connector.connect(user='yms',password='yms',host='120.24.81.151',database='easybp')

    columns = [i for i in dic.keys()]

    columns_str = "(" + ",".join(columns)  +")"

    values = [dic[k] for k in columns]

    values_str = "(" + ",".join(values)  +")"

    cur = conn.cursor()
    sql_statement = "INSERT INTO %s " %tableName + columns_str + " VALUES " + values_str

    print sql_statement

    cur.execute(sql_statement)

    conn.commit()

    conn.close()


