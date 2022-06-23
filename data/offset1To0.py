import sys

if len(sys.argv) >= 3:
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	with open(input_file, 'r') as f:
		content = f.readline()
		for line in f:
			line = line.strip('\n').split('\t')
			line[0] = int(line[0]) - 1
			line[0] = str(line[0])
			content += '\t'.join(line) + '\n'
	with open(output_file, 'w+') as f:
		f.write(content)
