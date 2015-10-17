import mysql.connector as connector



def insert_into_table(tableName,dic):
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


def delete_from_table(tableName,statement):
    conn = connector.connect(user='yms',password='yms',host='120.24.81.151',database='easybp')

    cur = conn.cursor()

    sql_statement = "DELETE FROM " + tableName + "WHERE" + statement

    cur.execute(sql_statement)

    conn.commit()

    conn.close()


def execute(stmt):
    result = None
    conn = connector.connect(user='yms',password='yms',host='120.24.81.151',database='easybp')

    cur = conn.cursor()

    cur.execute(stmt)

    try:
        result = cur.fetchall()
    except Exception:
        pass

    conn.commit()

    conn.close()

    return result

