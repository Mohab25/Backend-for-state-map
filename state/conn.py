import psycopg2 
# getting the hosiptals and snap them to closest vertices. 
# make a connection without refering to django ORM, using psycopg2
#
# initializing the connection  
connection = psycopg2.connect(host='localhost',database='state',user='mohab',password='m1k2h3')
    
def get_healthcare():
    """
        getting the hospitals from points.hospitals table through psycopg2, 
        get the closest lineString to each hospitals and extract it's source 
        vertex. 
        construct and return a list of vertices. 
    """
    # holders
    health_care = [] 
    lines_vertices=[]
    # getting the hospitals 
    with connection.cursor() as cur: 
        cur.execute('select * from points.hospitals')
        for i in cur: 
            health_care.append(i)
        # getting vertices most close to healthcare facilities, refer to KNN section: https://postgis.net/workshops/postgis-intro/knn.html
        for i in health_care:
            cur.execute(f"select id,source from lines.cleaned2 order by ST_Transform(lines.cleaned2.geom,4326) <->(select geom from points.hospitals where FID={i[0]}) limit 1 ")
            for i in cur:
                lines_vertices.append(i)
    return lines_vertices

def get_shortestPath(coords):
    """
        applying dijkstra to health care facilities vertices. return a geometry (refer to Mastering PostGIS). 
    """
    # getting the healthcare vertices. 
    source_vertices = get_healthcare()
    #holders 
    sources=[]
    shortest_paths=[]
    aggregations = []
    shortest_geom_holder=[]
    # find the closest vertices to coords
    with connection.cursor() as cur:
        cur.execute(f"select ST_AsText(ST_MakePoint({coords['lng']},{coords['lat']}),4326)")
        j=''
        closest_node=''
        for i in cur:
            j=i[0]
        cur.execute(f"select id,source from lines.cleaned2 order by ST_Transform(lines.cleaned2.geom,4326) <-> ST_GeomFromText('{j}',4326) limit 1")
        for i in cur:
            closest_node=i
        
    #getting the source of vertices only. 
    for i in source_vertices:
        sources.append(i[1])
    with connection.cursor() as cur:
        # each time the function runs, empty the previous result, which is a linestring geometry 
        cur.execute('delete from lines.dijkstra_results;')
        # this is the main part, dijkstra alogrithm.   
        for i in sources:
            looper=[]   # this is an array to divide each result comming from dijkstra for each facility  
            cur.execute(f"select pgr_dijkstra('select id,geom,source,target,ST_Length(geom) as cost from lines.cleaned2',{closest_node[1]},{i})") 
            for j in cur:
                looper.append(j)
            if looper!=[]:
                shortest_paths.append(looper)
        for i in shortest_paths:
            k = len(i)-1
            elem = i[k][0]    #this is the string which holds the aggregation value, taking the form of a tuple 
            aggregations.append(float(elem.split(",")[5].strip(')'))) 
        shortest = min(aggregations) # this is the aggregation value . 
        # now the last step is to get the line geometry from the aggregation value 
            # get pgr_dijkstra sequence of nodes that represents the shortest line sequence. 
        for i in shortest_paths:  # for each array that holds the values 
            k = len(i)-1
            elem = i[k][0]
            aggrey_cost=float((elem.split(",")[5].split(')'))[0]) 
            
            if aggrey_cost==shortest:
                shortest_geom_holder.append(i)
        nodes_holder=[]
        line_geom_parts_holder=[]
        for lines_list in shortest_geom_holder:
            for i in lines_list:
                tupler = eval(i[0])
                id1 = tupler[2]
                id2 = tupler[3]
                nodes_holder.append([id1,id2])
        lent = len(nodes_holder)-1   # getting the length of nodes holder to get the last pair, as the first node of the last pair is the hospital location  
        first_id = nodes_holder[0][0]
        last_id = nodes_holder[lent][0]
        cur.execute(f"select lines.cleaned2.geom from ( select * from pgr_dijkstra('select id,geom,source,target,ST_length(geom) as cost from lines.cleaned2', {first_id},{last_id})) as route left outer join lines.cleaned2 on id= route.edge")
        for i in cur:
            line_geom_parts_holder.append(i)
        # inserting newly created geometry to the empty table. 
        index=0
        returned_values='' # this will be returned to the view. 
        collector1=[]
        collector2=[]

        for i in line_geom_parts_holder:
            if(i[0]!=None):
                index+=1
                collector1.append(i)
            for i in collector1:
                cur.execute(f"select ST_AsText('{i[0]}')")
                for i in cur:
                    collector2.append(i[0])
            else:
                pass
        cur.execute(f'select ST_Collect(ARRAY{collector2})')
        for i in cur:
            returned_values=i[0]
        cur.execute(f"select ST_CollectionExtract(ST_GeomFromText(ST_AsText('{returned_values}')),2)")
        line=''
        for i in cur:
            last_line=i[0]
        cur.execute(f"insert into lines.dijkstra_results values({0},ST_SetSRID(ST_GeomFromText(ST_AsText('{last_line}')),32636))")
        cur.execute(f"select ST_Transform(ST_SetSRID(ST_GeomFromText(ST_AsText('{last_line}')),32636),4326)")
        for i in cur:
            adjust_line = i[0]
        connection.commit()
        return adjust_line

