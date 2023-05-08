import pickle
import leidenalg as la
import igraph as ig
import graph_tool.all as gt
from collections import Counter

filename = '2022-02-10_2022-02-23'

# Read network
g = ig.Graph.Read_GraphML('../networks/nato_' + filename + '.xml')
g.simplify(multiple = False, loops = True, combine_edges = None)
g.to_undirected(mode = "collapse", combine_edges = "sum")
g = g.clusters().giant()
g.write_graphml('../networks/nato_' + filename + '_gc.xml')
g_gc = gt.load_graph('../networks/nato_' + filename + '_gc.xml')
print('%d nodes and %d links in the giant component' % (g_gc.num_vertices(), g_gc.num_edges()))

# Run Leiden algorithm
best_entropy = 1000000
best_parts_dict = {}

for i in range(50):
	pv = {i:[] for i in range(g.vcount())}
	n_iter = 50
	for seed in range(n_iter):
		pt = la.RBConfigurationVertexPartition(g, weights = g.es["weight"], resolution_parameter = 0.28)
		la.Optimiser().set_rng_seed(seed)
		la.Optimiser().optimise_partition(pt, n_iterations = -1)
		for i in range(g.vcount()):
			pv[i].append(pt.membership[i])

	parts_dict = {}
	b = g_gc.new_vertex_property('int')
	for v in g_gc.vertices():
		counter = Counter(pv[int(v)])
		max_cls = counter.most_common(1)[0][0]
		if max_cls > 2:
			parts_dict[int(g_gc.vp['id'][v])] = 0
			b[v] = 0
		else:
			parts_dict[int(g_gc.vp['id'][v])] = max_cls
			b[v] = max_cls

	state = gt.BlockState(g_gc, b=b)
	print('Entropy: %.2f' % state.entropy())
	if state.entropy() < best_entropy:
		best_entropy = state.entropy()
		best_parts_dict = parts_dict

print('Best entropy: %.2f' % best_entropy)

with open('../data/parts_before_leiden.pkl', 'wb') as fp:
	pickle.dump(best_parts_dict, fp)
