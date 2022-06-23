# import re
from psutil import net_if_addrs
import sys

## Site
if len(sys.argv) >= 3:
    file_dSdN = sys.argv[1]
    file_dNdS = sys.argv[2]

    with open(file_dSdN, 'r') as f_in:
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
    print('Expected arguments: input_file output_file')

## Branch-site
# if len(sys.argv) >= 4:
#     # print('oui', sys.argv)
#     file_dN = sys.argv[1]
#     file_dS = sys.argv[2]
#     file_dNdS = sys.argv[3]
#     print(file_dN, '/', file_dS, '--->', file_dNdS)

#     # with open('fyco1/counts_pbps_dN.count', 'r') as fdn:
#     #     with open('fyco1/counts_pbps_dS.count', 'r') as fds:
#     #         with open('fyco1/counts_pbps_dNdS.count', 'w+') as fo:
#     with open(file_dN, 'r') as fdn:
#         with open(file_dS, 'r') as fds:
#             with open(file_dNdS, 'w+') as fo:
#                 content = ''
#                 n_header = fdn.readline()
#                 s_header = fds.readline()
#                 if n_header == s_header:
#                     content += n_header
#                 for line_n in fdn:
#                     line_s = fds.readline()
#                     line_n = line_n.strip('\n').split('\t')
#                     line_s = line_s.strip('\n').split('\t')
#                     print('n',line_n[0], '\ts',line_s[0])
#                     print(line_s)
#                     line_x = []
#                     for i in range(len(line_n)):
#                         if i == 0:
#                             line_x.append(line_n[i])
#                         else:
#                             line_x.append(f'{float(line_n[i])/float(line_s[i]):.4f}')
#                     content += '\t'.join(line_x)+'\n'
#                 fo.write(content)
# else:
#     print('Not enough arguments (dN input file, dS input file, dNdS output file)')
