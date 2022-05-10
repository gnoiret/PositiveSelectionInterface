import re
from psutil import net_if_addrs

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

# with open('ex2_SAMD9_YN98_dN.count', 'r') as fdn:
#     with open('ex2_SAMD9_YN98_dS.count', 'r') as fds:
#         with open('ex2_SAMD9_YN98_sitebranch.count', 'w+') as fo:
#             content = ''
#             n_header = fdn.readline()
#             s_header = fds.readline()
#             if n_header == s_header:
#                 content += n_header
#             for line_n in fdn:
#                 line_s = fds.readline()
#                 line_n = line_n.strip('\n').split('\t')
#                 line_s = line_s.strip('\n').split('\t')
#                 print('n',line_n[0], '\ts',line_s[0])
#                 print(line_s)
#                 line_x = []
#                 for i in range(len(line_n)):
#                     if i == 0:
#                         line_x.append(line_n[i])
#                     else:
#                         line_x.append(f'{float(line_n[i])/float(line_s[i]):.3f}')
#                 content += '\t'.join(line_x)+'\n'
#             fo.write(content)
