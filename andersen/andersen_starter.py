import andersen
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Wrong arguments, please use: python3 andersen_starter.py input_file_name output_file_name')
        exit()
    input_f = sys.argv[1]
    output_f = sys.argv[2]

    total_v, input_states = andersen.read_from_input(input_f)
    target_pairs = andersen.andersen_implement(input_states, total_v)
    andersen.write_to_output(output_f, target_pairs)

