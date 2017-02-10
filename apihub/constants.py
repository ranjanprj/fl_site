import psycopg2

cons_env = "cloud_dev"


def execute_sql(sql):
    try:
        conn = get_pg_conn()
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def fetch_sql(sql,fetchone = True):
    try:
        conn = get_pg_conn()
        c = conn.cursor()
        c.execute(sql)
        data = c.fetchone() if fetchone else c.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(e)

def pg_conn_str():
    if cons_env == "dev":
        dbname='apihub'
        user='postgres'
        host='localhost'
        password='postgres'
        conn_str = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname,user,host,password)
        return conn_str
    elif cons_env == "cloud_dev":
        dbname='apihub'
        user='postgres'
        host='ec2-52-90-180-17.compute-1.amazonaws.com'
        password='postgres'
        conn_str = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname,user,host,password)
        return conn_str


def get_pg_conn():
    conn_str = pg_conn_str()
    try:
        conn = psycopg2.connect(conn_str)
        return conn
    except Exception as e:
        print(e)
        print ("I am unable to connect to the database")



if __name__ == "__main__":
    data = fetch_sql("SELECT VERSION()")
    print(data)
