import sys

## Site
if len(sys.argv) >= 3:
    file_dS_dN = sys.argv[1]
    file_dNdS = sys.argv[2]
    
    with open(file_dS_dN, 'r') as f_in:
        with open(file_dNdS, 'w+') as f_out:
            content = ''
            f_in.readline()
            content += 'sites\tdNdS\n'
            for line in f_in:
                line = line.strip('\n').split('\t')
                dNdS = float(line[2])/float(line[1])
                content += f'{line[0]}\t{dNdS:.4f}\n'
            f_out.write(content)
else:
    print('Expected arguments: (dS dN) file, dN/dS file')
