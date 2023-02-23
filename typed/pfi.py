"""
ECS 240 Programming Assignment 2 

Precise Flow-Insensitive Points-to Analysis with WellDefined Types algorithm

Author: Xiang Hao, Siyuan Liu
"""

import io_types
import sys
import copy

# Statements:
# deref_l
# node_l
# deref_r
# node_r

G = {}
F = set()

def pfi(node_2_lvl, lvl_2_node, L, statements):

	for l in range(1, L + 1):
		
		v_ccp = []
		c_ccp = []

		# stype l r
		# stype = 0: var const
		# stype = 1: var var
		s_ccp = set()

		for statement in statements:
			[d, p, deref_r, z] = statement
			if deref_r == -1 and \
				node_2_lvl[z] == l - 1 and \
				node_2_lvl[p] == d + l:
				for q in lvl_2_node[l]:
					if len(find_all_paths(G, p, q)) > 0:
						s_ccp.add((0, q, z))

		for statement in statements:
			[d_1, p_1, deref_r, p_2] = statement

			if node_2_lvl[p_1] == l + d_1 and \
				deref_r >= 0 and \
				node_2_lvl[p_2] == l + deref_r:
				for q_1 in lvl_2_node[l]:
					for q_2 in lvl_2_node[l]:
						if q_1 == q_2:
							continue
						all_paths_1 = find_all_paths(G, q_1, p_1)
						all_paths_2 = find_all_paths(G, q_2, p_2)
						if exists_disjoint(all_paths_1, all_paths_2, F):
							s_ccp.add((1, q_1, q_2))

		lam = {}
		change = True
		for s in s_ccp:
			if s[0] == 0:
				if not (s[1] in lam):
					lam[s[1]] = s[2]
		for s in s_ccp:
			if s[0] == 1:
				lam[s[1]] = s[2]
		
		for lam_key in lam:
			if not (lam_key in G):
				G[lam_key] = set()
			G[lam_key].add(lam[lam_key])

		lam1 = set()
		for key in lam:
			lam1.add((key, lam[key]))

		lam2 = set()
		for s_x in s_ccp:
			if s_x[0] == 0:
				for s_y in s_ccp:
					if s_y[0] == 0 and s_x[1] != s_y[1]:
						lam2.add(((s_x[1], s_x[2]), (s_y[1], s_y[2])))
						lam2.add(((s_y[1], s_y[2]), (s_x[1], s_x[2])))
		
		change = True
		lam2_size = len(lam2)
		while change:
			change = False
			for element in lam2:
				element_X = element[0][0]
				element_small_x = element[0][1]
				element_Y = element[1][0]
				element_small_y = element[1][1]
				for z in s_ccp:
					if z[0] == 0 and z[1] != element_X:
						lam2.add(((element_X, element_small_x), (z[1], z[2])))
						lam2.add(((z[1], z[2]), (element_X, element_small_x)))
					if z[0] == 1 and z[2] == element_X and z[1] != element_X:
						lam2.add(((element_X, element_small_x), (z[1], element_small_x)))
						lam2.add(((z[1], element_small_x), (element_X, element_small_x)))
					if z[0] == 1 and z[2] == element_X and z[1] != element_Y:
						lam2.add(((z[1], element_small_x), (element_Y, element_small_y)))
						lam2.add(((element_Y, element_small_y), (z[1], element_small_x)))
			if lam2_size != len(lam2):
				change = True
			lam2_size = len(lam2)

		for lam1_s1 in lam1:
			for lam1_s2 in lam1:
				if lam1_s1[0] == lam1_s2[0]:
					continue
				if (((lam1_s1[0], lam1_s1[1]),(lam1_s2[0], lam1_s2[1])) not in lam2) and \
					(((lam1_s2[0], lam1_s2[1]),(lam1_s1[0], lam1_s1[1])) not in lam2):
					F.add(((lam1_s1[0], lam1_s1[1]),(lam1_s2[0], lam1_s2[1])) ) 
					F.add(((lam1_s2[0], lam1_s2[1]),(lam1_s1[0], lam1_s1[1])))
	return G

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths   

def exists_disjoint(paths1, paths2, f_pairs):
	for p1 in paths1:
		for p2 in paths2:
			p1_cp = copy.deepcopy(p1)
			p2_cp = copy.deepcopy(p2)
			p1_cp.reverse()
			p2_cp.reverse()
			is_dis = True
			for i in range(min(1, len(p1_cp), len(p2_cp))):
				if p1_cp[i] == p2_cp[i] or \
					((p1_cp[i], p1_cp[i - 1]), (p2_cp[i - 1], p2_cp[i - 1])) in f_pairs or \
					((p2_cp[i - 1], p2_cp[i - 1]), (p1_cp[i], p1_cp[i - 1])) in f_pairs:
					is_dis = False
					break
			if is_dis:
				return True
	return False

	#for l in layers[:-1]:
	#	statements = copy.copy(input_statements)
	#	# algorithm line 1-3
	#	V_ccp = [key for key, value in input_types.items() if value == l]
	#	C_ccp = [key for key, value in input_types.items() if value == l - 1]
	#	S_ccp = {}
	#	
	#	# algorithm line 4
	#	for s in range(statements['right']):
	#		if statements['right'][s][0] == -1:
	#			for q in V_ccp:
	#				for k in range(statements['right']):
	#					if statements['left'][k][1] == statements['left'][s][1] and statements['right'][k][1] == q and statements['right'][k][0] == -1:
	#						S_ccp[q] = statements['right'][1]
	#	
	#	# algorithm line 5
	#	forbidden_pairs = {}
	#	
	#	# algorithm line 6
	#	pairs_of_V_ccp = [((i), (i+1) % len(V_ccp)) for i in range(len(V_ccp))]
	#	for s in range(statements['right']):
	#		if statements['left'][s][0] > 1 and statements['right'][s][0] > 1:
	#			for pair in range(pairs_of_V_ccp):
					


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Wrong arguments, please use: python3 io.py input_file_name output_file_name')
		exit()
		
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	
	input_nodes, input_types, input_statements = io_types.read_from_types("typed/tests/p1.txt")
	
	
	