import pickle
from graph_tool.all import *

filename = '2022-02-10_2022-02-23'

hl_colors = ['#001DA1', '#F745B3']  # Dark blue, magenta
bg_colors = ['#9DC742', '#f4bd1c']  # Green, yellow
gray_color = '#AAAAAA'
dark_gray_color = '#5B5B5B'
light_gray_color = '#CCCCCC'
border_color = '#404040'

g = load_graph('../networks/' + filename + '.xml.gz')
g.set_directed(False)
remove_self_loops(g)
g_filt = GraphView(g, vfilt=label_largest_component(g))

pos = sfdp_layout(g_filt)
g_filt.vp.pos = pos

g_filt.ep['edge_width'] = g_filt.new_edge_property('double')
for e in g_filt.edges():
	e_weight = g_filt.ep['weight'][e]
	g_filt.ep['edge_width'][e] = 0.4 * (e_weight ** 0.5)

"""
Plot uncolored network
"""
graph_draw(g_filt, pos=g_filt.vp.pos, output_size=(1000,1000),
	vertex_color=[1,1,1,0.3], vertex_fill_color=[0,0,0,0.8], vertex_size=2.5, 
	edge_color=[0/255,0/255,0/255,0.4], 
	edge_pen_width=g_filt.ep['edge_width'], vertex_pen_width=0.5, 
	output='../figures/' + filename + '.png')

# """
# Plot colored network
# """
# with open('../data/user_list.pkl', 'rb') as fp:
# 	user_list = pickle.load(fp)
# with open('../data/parts_before_leiden.pkl', 'rb') as fp:
# 	parts_dict = pickle.load(fp)

# g_filt.vp.color = g_filt.new_vertex_property('string')
# g_filt.vp.order = g_filt.new_vertex_property('int')
# g_filt.vp.shape = g_filt.new_vertex_property('int')
# g_filt.vp.size = g_filt.new_vertex_property('double')
# g_filt.vp.outline = g_filt.new_vertex_property('double')
# g_filt.vp.subset = g_filt.new_vertex_property('bool')
# for v in g_filt.vertices():
# 	user_id = int(user_list[int(g_filt.vp._graphml_vertex_id[int(v)])])
# 	if user_id not in parts_dict:
# 		g_filt.vp.order[v] = 0
# 		g_filt.vp.size[v] = 3
# 		g_filt.vp.shape[v] = 0
# 		g_filt.vp.outline[v] = 0.5
# 		g_filt.vp.color[v] = gray_color
# 		g_filt.vp.subset[v] = False
# 	elif parts_dict[user_id] == 0:
# 		g_filt.vp.order[v] = 1
# 		g_filt.vp.size[v] = 4.5
# 		g_filt.vp.shape[v] = 0
# 		g_filt.vp.outline[v] = 0.8
# 		g_filt.vp.color[v] = bg_colors[0]
# 		g_filt.vp.subset[v] = True
# 	elif parts_dict[user_id] == 1:
# 		g_filt.vp.order[v] = 2
# 		g_filt.vp.size[v] = 9
# 		g_filt.vp.shape[v] = 1
# 		g_filt.vp.outline[v] = 0.8
# 		g_filt.vp.color[v] = hl_colors[0]
# 		g_filt.vp.subset[v] = True
# 	else:
# 		g_filt.vp.order[v] = 3
# 		g_filt.vp.size[v] = 8.5
# 		g_filt.vp.shape[v] = 2
# 		g_filt.vp.outline[v] = 0.8
# 		g_filt.vp.color[v] = hl_colors[1]
# 		g_filt.vp.subset[v] = True

# graph_draw(g_filt, pos=pos, output_size=(1000,1000),
# 	vertex_color=[255/255,255/255,255/255,0.8], vertex_fill_color=g_filt.vp.color, vertex_size=g_filt.vp.size, vorder=g_filt.vp.order, vertex_shape=g_filt.vp.shape,
# 	edge_color=[200/255,200/255,200/255,0.25], 
# 	edge_pen_width=g_filt.ep['edge_width'], vertex_pen_width=g_filt.vp.outline, 
# 	output='../figures/' + filename + '_colored.png')