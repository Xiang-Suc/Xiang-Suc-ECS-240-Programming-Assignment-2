import sys
import copy
import pfi

# input_nodes: [1, 2, 3, 4, 5, 6, 7, 8]
# input_types: {1: 3,
#               2: 3,
#               3: 2,
#               4: 2,
#               5: 1,
#               6: 1,
#               7: 0,
#               8: 0}
# input_statements: {left: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (2, 1)],
#                    right: [(-1, 3), (-1, 4), (-1, 5), (-1, 6), (-1, 7), (-1, 8), (2, 2)]}

def read_from_types(filename):
    file = open(filename, 'r')
    read = file.readlines()
    node_2_lvl = {};
    lvl_2_node = {}
    L = -1
    statements = []

    for line in read:
        # p n s
        if line.startswith('p'):
            points = line.split(' ')
            n = int(points[1])
            num_statement = int(points[2])
    
        # t u i
        if line.startswith('t'):
            indexs = line.split()
            node = int(indexs[1])
            level = int(indexs[2])
            node_2_lvl[node] = level
            if not (level in lvl_2_node):
                lvl_2_node[level] = set()
            lvl_2_node[level].add(node)
            L = max(L, level)

        # s d1 v1 d2 v2
        if line.startswith('s'):
            keys = line.split(' ')
            deref_l = int(keys[1])
            node_l = int(keys[2])
            deref_r = int(keys[3])
            node_r = int(keys[4])
            statements.append([deref_l, node_l, deref_r, node_r])
            
        # c . . .
        if line.startswith('c'):
            continue
    file.close()
        
    return node_2_lvl, lvl_2_node, L, statements


# pt 1 3
# pt 2 4
# pt 3 5
# pt 4 6
# pt 5 7
# pt 5 8
# pt 6 8
def write_to_output(filename, realizable_pairs):
    file = open(filename, 'w')
    if realizable_pairs is None:
        file.write('\n')
    else:
        for i in realizable_pairs:
            for val in realizable_pairs[i]:
                file.write('pt ' + str(i) + ' ' + str(val) + '\n')

    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Wrong arguments, please use: python3 io.py input_file_name output_file_name')
        exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    node_2_lvl, lvl_2_node, L, statements = read_from_types(input_file)

    g = pfi.pfi(node_2_lvl, lvl_2_node, L, statements)


    realizable_pairs = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 5: 8, 6: 8} 
    write_to_output(output_file, g )
    
    