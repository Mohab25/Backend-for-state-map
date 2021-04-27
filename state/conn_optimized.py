# make the connection 
import psycopg2
connection = psycopg2.connect(host='localhost',database='state',user='mohab',password='m1k2h3')

def get_healthcare():
    """
        getting the hospitals from points.hospitals table through psycopg2, 
        return: list of health care facilities. 
    """
    # holders
    health_care = [] 
    # getting the hospitals 
    with connection.cursor() as cur: 
        cur.execute('select * from points.hospitals')
        for i in cur: 
            health_care.append(i)
    return health_care

def health_care_source_nodes():
    """
    get the health care facilities from the previous cell, then extract the closest node in the graph(network) 
    to each facility.
    use limit to return only one node for each hospital.
    using select id,source will return only the id and the source node (number).
    the <-> operator is the k nearest neighbour (between two geometries) refer to KNN section: https://postgis.net/workshops/postgis-intro/knn.html
    return: list of id and sources of the graph source nodes.
    """
    lines_vertices=[] #holder
    healthcare_facilities = get_healthcare()
    with connection.cursor() as cur: # this code actually needs refactor, limit the calls to the database to one
        for i in healthcare_facilities:
            cur.execute(f"select id,source from lines.cleaned2 order by ST_Transform(lines.cleaned2.geom,4326) <->(select geom from points.hospitals where FID={i[0]}) limit 1 ")
            for i in cur:
                lines_vertices.append(i)
    return lines_vertices

def snap_point_to_nearest_vertex(coords):
    """
    As the dijkstra alogrithm works only with the points on the graph, you want to snap the click coordinate 
    to nearest point on the graph.
    first create the point geometry from the coords (decimal deg) and find the KNN.
    return: id and source of the closest point to where the user clicks on the map.
    """
    with connection.cursor() as cur:
    # point creation
        cur.execute(f"select ST_AsText(ST_MakePoint({coords['lng']},{coords['lat']}),4326)")
        j=''
        closest_node=''
        for i in cur:
            j=i[0]
        cur.execute(f"select id,source from lines.cleaned2 order by ST_Transform(lines.cleaned2.geom,4326) <-> ST_GeomFromText('{j}',4326) limit 1")
        for i in cur:
            closest_node=i
    return closest_node

def dijkstra(coords):
    source_nodes = [i[1] for i in health_care_source_nodes()]
    nearest_snap = snap_point_to_nearest_vertex(coords)
    results=[]
    with connection.cursor() as cur:
        cur.execute(f"select pgr_dijkstra('select id,geom,source,target,ST_Length(geom) as cost from lines.cleaned2',{nearest_snap[1]},ARRAY{source_nodes},FALSE)") 
        for i in cur:
            results.append(i)
    return results

def compare_edges(coords):
    """
    compare the aggregation costs of the different shortest paths obtained from dijkstra to multiple points
    to find which one of these shortest paths is has the minimum value. 
    pgr_dijkstra returns the shortest path aggregation value on the last tuple of a certain path (see my doc - understaing postgis dijkstra functions results)
    where the end point will be the same and the end_vid [3rd element of the tuple index=2] will be the same as the node [4th element], and edge [5th element] =-1 and cost =0
    """
    dijkstra_results = dijkstra(coords)
    aggregation_costs=[] # holding the cost.
    aggregation_costs_edges=[] # holding the cost and the id of the end point.
    for i in dijkstra_results: # tuple holding two elements, a tuple and an empty entery
            j=eval(i[0])
            if j[2]==j[3] and j[4]==-1:
                cost = j[6]
                aggregation_costs.append(cost)
                aggregation_costs_edges.append((j[3]))
    # getting the index of the min value of aggregation_costs 
    shortest_length_index = aggregation_costs.index(min(aggregation_costs))
    # getting the node closest to the closest facility
    closest_node = aggregation_costs_edges[shortest_length_index]
    # now i need to return all of the edges which has this value as it's end_vid to construct the shortest path. (for fun you can return nodes of the shortest path )
    edges_of_shorest_path=[]
    for i in dijkstra_results:
        j=eval(i[0])
        if j[2]==closest_node:
            edges_of_shorest_path.append(j[4])
    return edges_of_shorest_path

def construct_shortest_path(coords):
    shortest_path_edges = compare_edges(coords)
    #exclude the last edge which is -1 
    shortest_path_edges.remove(-1)
    geoms = []
    with connection.cursor() as cur:
        cur.execute(f"select lines.cleaned2.geom from unnest(ARRAY{shortest_path_edges}) as route left outer join lines.cleaned2 on id= route")
        for i in cur:
            geoms.append(i[0])
    return geoms

def geom_as_json(coords):
    geoms = construct_shortest_path(coords)
    json_geoms = []
    with connection.cursor() as cur:
        cur.execute(f"select ST_AsGeoJSON(ST_Transform(ST_Collect(ARRAY{geoms}),4326))")
        for i in cur:
            json_geoms.append(i)

    return json_geoms