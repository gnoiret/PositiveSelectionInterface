import sys

if len(sys.argv) >= 2:
	input_files = sys.argv[1:]
	for input_file in input_files:
		with open(input_file, 'r') as f:
			content = f.readline()
			for line in f:
				line = line.strip('\n').split('\t')
				line[0] = int(line[0]) - 1
				line[0] = str(line[0])
				content += '\t'.join(line) + '\n'
		with open(f'{input_file}_offset.txt', 'w+') as f:
			f.write(content)
