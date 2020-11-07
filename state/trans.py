import psycopg2 
import binascii 

conn = psycopg2.connect(host='localhost',database='state',user='mohab',password='m1k2h3')

with conn.cursor() as cur:
    geoms =[]
    geoms_with_srid=[]
    cur.execute('select ST_AsText(geom) from state_pau')
    for i in cur:
        geoms.append(i)
    for i in geoms:
        cur.execute(f"select ST_SetSRID(ST_GeomFromText('{i[0]}'),3857)")
    for i in cur:
        print(i)
        #cur.execute(f"insert into state_pau values()")





        #3857