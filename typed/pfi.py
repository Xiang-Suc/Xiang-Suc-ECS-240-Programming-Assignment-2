"""
ECS 240 Programming Assignment 2 

Precise Flow-Insensitive Points-to Analysis with WellDefined Types algorithm

Author: Xiang Hao, Siyuan Liu
"""

import io_types
import sys
import copy


def realizable_pairs(input_nodes, input_types, input_statements):
	# get the number of layers L
	key = max(input_types, key= lambda x: input_types[x])
	max_value = input_types[key]
	layers = [max_value - i for i in range(max_value+1)]
	print(layers)
	print(input_statements)	
	
	for l in layers[:-1]:
		statements = copy.copy(input_statements)
		# algorithm line 1-3
		V_ccp = [key for key, value in input_types.items() if value == l]
		C_ccp = [key for key, value in input_types.items() if value == l - 1]
		S_ccp = {}
		
		# algorithm line 4
		for s in range(statements['right']):
			if statements['right'][s][0] == -1:
				for q in V_ccp:
					for k in range(statements['right']):
						if statements['left'][k][1] == statements['left'][s][1] and statements['right'][k][1] == q and statements['right'][k][0] == -1:
							S_ccp[q] = statements['right'][1]
		
		# algorithm line 5
		forbidden_pairs = {}
		
		# algorithm line 6
		pairs_of_V_ccp = [((i), (i+1) % len(V_ccp)) for i in range(len(V_ccp))]
		for s in range(statements['right']):
			if statements['left'][s][0] > 1 and statements['right'][s][0] > 1:
				for pair in range(pairs_of_V_ccp):
					


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Wrong arguments, please use: python3 io.py input_file_name output_file_name')
		exit()
		
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	
	input_nodes, input_types, input_statements = io_types.read_from_types("typed/tests/p1.txt")
	
	
	