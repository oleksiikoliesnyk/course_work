import psycopg2

conn = psycopg2.connect(host="localhost", port = 5432, database="University", user="postgres", password="i183")
cur = conn.cursor()
cur.execute("""SELECT * FROM student""")
query_results = cur.fetchall()
print(query_results)
