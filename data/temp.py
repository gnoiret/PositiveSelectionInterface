# import re
from psutil import net_if_addrs
import sys

# with open('ex2_SAMD9_YN98_dNdS.count', 'r') as fi:
#     with open('ex2_SAMD9_YN98_omega.count', 'w+') as fo:
#         content = ''
#         fi.readline()
#         content += 'sites\tomega\n'
#         for line in fi:
#             line = line.strip('\n').split('\t')
#             omega = float(line[2])/float(line[1])
#             content += f'{line[0]}\t{omega:.8f}\n'
#         fo.write(content)

if len(sys.argv) >= 4:
    # print('oui', sys.argv)
    file_dN = sys.argv[1]
    file_dS = sys.argv[2]
    file_dNdS = sys.argv[3]
    print(file_dN, '/', file_dS, '--->', file_dNdS)

    # with open('fyco1/counts_pbps_dN.count', 'r') as fdn:
    #     with open('fyco1/counts_pbps_dS.count', 'r') as fds:
    #         with open('fyco1/counts_pbps_dNdS.count', 'w+') as fo:
    with open(file_dN, 'r') as fdn:
        with open(file_dS, 'r') as fds:
            with open(file_dNdS, 'w+') as fo:
                content = ''
                n_header = fdn.readline()
                s_header = fds.readline()
                if n_header == s_header:
                    content += n_header
                for line_n in fdn:
                    line_s = fds.readline()
                    line_n = line_n.strip('\n').split('\t')
                    line_s = line_s.strip('\n').split('\t')
                    print('n',line_n[0], '\ts',line_s[0])
                    print(line_s)
                    line_x = []
                    for i in range(len(line_n)):
                        if i == 0:
                            line_x.append(line_n[i])
                        else:
                            line_x.append(f'{float(line_n[i])/float(line_s[i]):.3f}')
                    content += '\t'.join(line_x)+'\n'
                fo.write(content)
else:
    print('Not enough arguments (dN input file, dS input file, dNdS output file)')
