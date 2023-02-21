import sys
import copy

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
    input_nodes = []
    input_types = {}
    input_statements = {}
    left_list = []
    right_list = []    

    for line in read:
        # p n s
        if line.startswith('p'):
            points = line.split(' ')
            n = int(points[1])
            num_statement = int(points[2])
    
        # t u i
        if line.startswith('t'):
            indexs = line.split(' ')
            node = int(indexs[1])
            num_stars = int(indexs[2])
            input_types[node] = num_stars
            
        # s d1 v1 d2 v2
        if line.startswith('s'):
            keys = line.split(' ')
            left_num_star = int(keys[1])
            left_node = int(keys[2])
            right_prefix = int(keys[3])
            right_node = int(keys[4])
            
            left_list.append(copy.copy((left_num_star, left_node)))
            right_list.append(copy.copy((right_prefix, right_node)))
            
        # c . . .
        if line.startswith('c'):
            continue
    input_statements['left'] = left_list
    input_statements['right'] = right_list
    file.close()
    
    for i in range(n):
        input_nodes.append(i+1)
        
    return input_nodes, input_types, input_statements


# pt 1 3
# pt 2 4
# pt 3 5
# pt 4 6
# pt 5 7
# pt 5 8
# pt 6 8
def write_to_output(filename, realizable_pairs):
    file = open(filename, 'w')
    for i in realizable_pairs:
        if realizable_pairs is None:
            file.write('\n')
        else:
            file.write('pt ' + str(i) + ' ' + str(realizable_pairs[i]) + '\n')

    file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Wrong arguments, please use: python3 io.py input_file_name output_file_name')
        exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    input_nodes, input_types, input_statements = read_from_types(input_file)
    realizable_pairs = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 5: 8, 6: 8} 
    print(input_nodes)
    print(input_types)
    print(input_statements)

    write_to_output(output_file, realizable_pairs)
