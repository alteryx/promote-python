import psycopg2

# create a DB function
def get_db_data(user_id):
    """
    This function opens a connection to a Postgres DB
    and returns the user information with the matching `user_id`
    """
    data = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="promote",
            user="promote",
            password=os.environ["DB_PASSWORD"],
            port=5444)
    except:
        print("Unable to connect to the database")

    q = "select * from users where username='{get_user_id}';".format(get_user_id = user_id)
    cur = conn.cursor()
    try:
        # as an example of the timeout, the "pg_sleep" statement will fail
        #cur.execute("select pg_sleep(2000)")
        cur.execute(q)
        data = cur.fetchall()
    except:
        print("failed to execute query")
    # close our connection
    conn.close()
    return data
