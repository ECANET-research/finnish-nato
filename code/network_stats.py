import pickle
import graph_tool.all as gt

filename = '2022-02-10_2022-02-23'

with open('../data/user_list.pkl', 'rb') as fp:
	user_list = pickle.load(fp)
with open('../data/parts_before_leiden.pkl', 'rb') as fp:
	parts_dict = pickle.load(fp)

main_users = set()
blue_users = set()
red_users = set()
for u in parts_dict:
	if parts_dict[u] == 0:
		main_users.add(u)
	elif parts_dict[u] == 1:
		blue_users.add(u)
	else:
		red_users.add(u)

"""
Read network
"""
g = load_graph('../networks/' + filename + '.xml.gz')
gt.remove_self_loops(g)
g_copy = gt.load_graph('../networks/' + filename + '.xml.gz')
g_copy.set_directed(False)
gt.remove_self_loops(g_copy)
g_gc = gt.GraphView(g_copy, vfilt=gt.label_largest_component(g_copy))


"""
Count number of nodes and edges
"""
node_cnt = {0:0, 1:0, 2:0}

g.vp.subset = g.new_vertex_property('bool')
g.vp.b = g.new_vertex_property('int')
for v in g_gc.vertices():
	user_id = int(user_list[int(g.vp._graphml_vertex_id[int(v)])])
	if user_id not in parts_dict:
		g.vp.subset[v] = False
		g.vp.b[v] = -1
	else:
		g.vp.subset[v] = True
		g.vp.b[v] = parts_dict[user_id]
		node_cnt[parts_dict[user_id]] += 1
print(node_cnt)

# g_subset = gt.GraphView(g, vfilt=g.vp.subset)
# state = gt.BlockState(g_subset, b=g_subset.vp.b)
# m = state.get_matrix()
# print(m.todense())

edge_cnt = {('red', 'red'):0, ('red', 'main'):0, ('blue', 'blue'):0, ('blue', 'main'):0, 'red':0, 'blue':0}
for e in g.edges():
	from_user = int(user_list[int(g.vp._graphml_vertex_id[int(e.source())])])
	to_user = int(user_list[int(g.vp._graphml_vertex_id[int(e.target())])])
	if e.source() in g_gc.vertices() and e.target() in g_gc.vertices():
		if from_user in red_users:
			edge_cnt['red'] += g.ep['weight'][e]
			if to_user in red_users:
				edge_cnt[('red', 'red')] += g.ep['weight'][e]
			if to_user in main_users:
				edge_cnt[('red', 'main')] += g.ep['weight'][e]
		if from_user in blue_users:
			edge_cnt['blue'] += g.ep['weight'][e]
			if to_user in blue_users:
				edge_cnt[('blue', 'blue')] += g.ep['weight'][e]
			if to_user in main_users:
				edge_cnt[('blue', 'main')] += g.ep['weight'][e]
print(edge_cnt)