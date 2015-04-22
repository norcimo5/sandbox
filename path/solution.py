def find_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

def solve(map, miner, exit):
	max_rows = len(map)
	max_cols = len(map[0])
	route = {}
	offset = lambda x, y: x + y * max_cols
	is_square = lambda x, y: map[x][y] \
	if x >=0 and x < max_rows \
	and y >=0 and y < max_cols  else False
	for i in range (0, max_rows):
		for j in range (0, max_cols):
			if is_square(i, j) == True:
				d = []
				if is_square(i, j-1) : d.append(offset(i,j-1))
				if is_square(i, j+1) : d.append(offset(i,j+1))
				if is_square(i-1, j) : d.append(offset(i-1,j))
				if is_square(i+1, j) : d.append(offset(i+1,j))
				route[offset(i,j)] = d
                
	result = min(find_paths(route, offset(miner['x'], miner['y']), offset(exit['x'], exit['y'])))           
	if result == [0]: return []
    
	prev = result[0]
	r = []
    
	direction = { -1:"left", 1:"right", max_rows:"down", -max_rows:"up"}
	for i in range(1, len(result)):
		r.append(direction.get(result[i] - prev))
		prev = result[i]
        
	return r
