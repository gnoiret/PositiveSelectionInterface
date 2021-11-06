import sys

def dna_to_prot(dna_seq:str):
    matches = {
        'TTT':'F', 'TTC':'F', 'TTA':'L', 'TTG':'L',
        'TCT':'S', 'TCC':'S', 'TCA':'S', 'TCG':'S', 
        'TAT':'Y', 'TAC':'Y', 'TAA':'*', 'TAG':'*',
        'TGT':'C', 'TGC':'C', 'TGA':'*', 'TGG':'W',
        
        'CTT':'L', 'CTC':'L', 'CTA':'L', 'CTG':'L',
        'CCT':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P',
        'CAT':'H', 'CAC':'H', 'CAA':'Q', 'CAG':'Q',
        'CGT':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R',

        'ATT':'I', 'ATC':'I', 'ATA':'I', 'ATG':'M',
        'ACT':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T',
        'AAT':'N', 'AAC':'N', 'AAA':'K', 'AAG':'K',
        'AGT':'S', 'AGC':'S', 'AGA':'R', 'AGG':'R',
        
        'GTT':'V', 'GTC':'V', 'GTA':'V', 'GTG':'V',
        'GCT':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A',
        'GAT':'D', 'GAC':'D', 'GAA':'E', 'GAG':'E',
        'GGT':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G',

        '---':'-',
    }
    aa = ''
    # print(dna_seq)
    if len(dna_seq)%3 == 0:
        codons = [dna_seq[i:i+3].upper() for i in range(0, len(dna_seq), 3)]
        # print('codons:', codons)
        for codon in codons:
            codon = codon.replace('U', 'T')
            try:
                aa += matches[codon]
            except KeyError:
                print(f'/!\\ Unknown codon: {codon}, translation aborted')
        # print('aa:', aa)
        return aa
    else:
        print('/!\\ Inorrect length for dna_seq')
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        seq = sys.argv[1]
        print(dna_to_prot(seq))
    # dna_to_prot('ATGTGCCTGGGCTGCTGA')
    # dna_to_prot('ATGTGCCTGGGCUGC')
    # dna_to_prot('ATGTGCCTGGGCBBB')
