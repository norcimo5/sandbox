#!/usr/bin/python

def shabama(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = shabama(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

minemap = [[True, True, True], [False, False, True], [True, True, True]]
max_rows = len(minemap)
max_cols = len(minemap[0])
offset = lambda x, y: x + y * max_cols
is_square = lambda x, y: minemap[x][y] \
            if x >=0 and x < max_rows \
            and y >=0 and y < max_cols \
            else False
m_route = {}

for i in range (0, max_rows):
    for j in range (0, max_cols):
        if is_square(i, j) == True:
            print offset(i,j)
            d = []
            print i, j
            if is_square(i, j-1) == True : d.append(offset(i,j-1))
            if is_square(i, j+1) == True : d.append(offset(i,j+1))
            if is_square(i-1, j) == True : d.append(offset(i-1,j))
            if is_square(i+1, j) == True : d.append(offset(i+1,j))
            m_route[offset(i,j)] = d

print m_route
print min(shabama(m_route, 0, 2))
