# c This is a comment.
# p 3 4
# c 1 = &2
# s 0 1 -1 2
# c 2 = &3
# s 0 2 -1 3
# c 3 = &1
# s 0 3 -1 1
# c 2 = 1
# s 0 2 0 1
# c This is another comment.
def read_from_input(filename):
    total_v = 0
    add_v = 0
    input_states = {'&': set(), '=': set(), 'r*': set(), 'l*': set()}
    file = open(filename, 'r')
    read = file.readlines()

    for line in read:
        # p N S
        if line.startswith('p'):
            split_p = line.split(' ')
            total_v = int(split_p[1])
            add_v = total_v + 1
        # s d1 v1 d2 v2
        elif line.startswith('s'):
            split_s = line.split(' ')
            d1 = int(split_s[1])
            v1 = int(split_s[2])
            d2 = int(split_s[3])
            v2 = int(split_s[4])
            statement_helper(d1, v1, d2, v2, add_v, input_states)
        # c ...
        else:
            continue
    return total_v, input_states


def statement_helper(d1, v1, d2, v2, add_v, input_states):
    if d1 == 0:
        # d1 == 0, d2 == -1
        if d2 == -1:
            input_states['&'].add((v1, v2))
        # d1 == 0, d2 == 0
        elif d2 == 0:
            input_states['='].add((v1, v2))
        # d1 == 0, d2 > 0
        else:
            left = add_v
            right = v2
            for i in range(0, d2 - 1):
                input_states['r*'].add((left, right))
                right = left
                add_v += 1
                left = add_v
            input_states['r*'].add((v1, right))
    else:
        # d1 > 0, d2 == -1
        if d2 == -1:
            left = add_v
            right = v1
            for i in range(0, d1):
                input_states['r*'].add((left, right))
                right = left
                add_v += 1
                left = add_v
            input_states['&'].add((right, v2))
        # d1 > 0, d2 == 0
        elif d2 == 0:
            left = add_v
            right = v1
            for i in range(0, d1 - 1):
                input_states['r*'].add((left, right))
                right = left
                add_v += 1
                left = add_v
            input_states['l*'].add((right, v2))
        # d1 > 0, d2 > 0
        else:
            if d1 > d2:
                l_left = add_v
                l_right = v1
                for i in range(0, d1 - 1):
                    input_states['r*'].add((l_left, l_right))
                    l_right = l_left
                    add_v += 1
                    l_left = add_v

                r_left = add_v
                r_right = v2
                for i in range(0, d2):
                    input_states['r*'].add((r_left, r_right))
                    r_right = r_left
                    add_v += 1
                    r_left = add_v
                input_states['l*'].add((l_right, r_right))

            elif d1 == d2:
                l_left = add_v
                l_right = v1
                for i in range(0, d1 - 1):
                    input_states['r*'].add((l_left, l_right))
                    l_right = l_left
                    add_v += 1
                    l_left = add_v

                r_left = add_v
                r_right = v2
                for i in range(0, d2):
                    input_states['r*'].add((r_left, r_right))
                    r_right = r_left
                    add_v += 1
                    r_left = add_v
                input_states['l*'].add((l_right, r_right))

            else:
                l_left = add_v
                l_right = v1
                for i in range(0, d1):
                    input_states['r*'].add((l_left, l_right))
                    l_right = l_left
                    add_v += 1
                    l_left = add_v

                r_left = add_v
                r_right = v2
                for i in range(0, d2 - 1):
                    input_states['r*'].add((r_left, r_right))
                    r_right = r_left
                    add_v += 1
                    r_left = add_v
                input_states['r*'].add((l_right, r_right))


def write_to_output(filename, target_pairs):
    file = open(filename, 'w')
    for pair in target_pairs:
        file.write('pt ' + str(pair[0]) + ' ' + str(pair[1]) + '\n')
    file.close()


def andersen_implement(input_states, total_v):
    points_pairs = set()
    changed = True
    while changed:
        current_pairs = points_pairs.copy()
        before_size = len(current_pairs)
        changed = False
        # x = & y -> <x , y> T
        for t1 in input_states['&']:
            points_pairs.add(t1)

        # x = y, <y, z> T -> <x, z> T
        for t2 in input_states['=']:
            x = t2[0]
            y = t2[1]
            for temp in current_pairs:
                v1 = temp[0]
                v2 = temp[1]
                if y == v1:
                    # print((x, v2))
                    points_pairs.add((x, v2))

        # x = * y, <y, w> T, <w, z> T -> <x, z> T
        for t3 in input_states['r*']:
            x = t3[0]
            y = t3[1]
            for temp1 in current_pairs:
                v1 = temp1[0]
                v2 = temp1[1]
                for temp2 in current_pairs:
                    v3 = temp2[0]
                    v4 = temp2[1]
                    if y == v1 and v2 == v3:
                        # print((x, v4))
                        points_pairs.add((x, v4))

        # * x = y, <x, w> T, <y, z> T -> <w, z> T
        for t4 in input_states['l*']:
            x = t4[0]
            y = t4[1]
            for temp1 in current_pairs:
                v1 = temp1[0]
                v2 = temp1[1]
                for temp2 in current_pairs:
                    v3 = temp2[0]
                    v4 = temp2[1]
                    if x == v1 and y == v3:
                        # print((v2, v4))
                        points_pairs.add((v2, v4))

        if len(points_pairs) > before_size:
            # print(len(points_pairs))
            changed = True

    # print(points_pairs)
    target_pairs = target_filter(points_pairs, total_v)
    return target_pairs


def target_filter(points_pairs, total_v):
    target_pairs = set()
    for pair in points_pairs:
        v1 = pair[0]
        v2 = pair[1]
        if v1 <= total_v and v2 <= total_v:
            target_pairs.add(pair)
    return target_pairs


if __name__ == '__main__':
    total_v1, input_states1 = read_from_input("tests/p1.txt")
    print(total_v1)
    print(input_states1)
    target_pairs1 = andersen_implement(input_states1, total_v1)
    print(target_pairs1)
    print(" ")

    total_v2, input_states2 = read_from_input("tests/p2.txt")
    print(total_v2)
    print(input_states2)
    target_pairs2 = andersen_implement(input_states2, total_v2)
    print(target_pairs2)
    print(" ")

    total_v3, input_states3 = read_from_input("tests/p3.txt")
    print(total_v3)
    print(input_states3)
    target_pairs3 = andersen_implement(input_states3, total_v3)
    print(target_pairs3)
    print(" ")

    total_v4, input_states4 = read_from_input("tests/p4.txt")
    print(total_v4)
    print(input_states4)
    target_pairs4 = andersen_implement(input_states4, total_v4)
    print(target_pairs4)
    print(" ")

    write_to_output("output.txt", target_pairs4)

