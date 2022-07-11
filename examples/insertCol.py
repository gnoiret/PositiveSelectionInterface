import sys

if len(sys.argv) >= 4:
    input_file = sys.argv[1]
    col_index = sys.argv[2]
    col_header = sys.argv[3]
    col_content = sys.argv[4]
    output_file = input_file+'_insert.txt'

    with open(input_file, 'r') as f_in:
        with open(output_file, 'w+') as f_out:
            content = ''
            header = f_in.readline()
            header = header.strip().split('\t')
            header.insert(int(col_index), col_header)
            content += '\t'.join(header) + '\n'
            for line in f_in:
                line = line.strip().split('\t')
                line.insert(int(col_index), col_content)
                content += '\t'.join(line) + '\n'
            f_out.write(content)
else:
    print('Expected arguments: input file, column index, column header, column content')
