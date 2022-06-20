# Part of this  code is taken from https://groups.google.com/forum/#!topic/etetoolkit/cYTHHsL21KY
# written by Jaime Huerta-Cepas

"""
Ecrit un  arbre au format XML .
Usage:
  genere_xml.py <treeFile> <alignmentFile> <resultsFile>

Positional arguments:
  treeFile              family name / phylogenic trees in newick format
  alignmentFile         multiple alignment in fasta format
  resultsFile           statistics

"""

import argparse
# import json
from modulefinder import AddPackagePath
import sys
import re
import random
import os
from Bio import Phylo
from io import StringIO
# import time
# from ete3 import Phyloxml, phyloxml

from lxml import etree
from xml.etree import ElementTree
from xml.dom import minidom

from lxml.etree import XMLParser, parse

# from docopt import docopt
# import sqlite3
# import zlib
# import base64

# args = docopt(__doc__)
# tree = args["<treeFile>"]
# alignment = args["<alignmentFile>"]
# results = args["<resultsFile>"]
# arguments = docopt(__doc__, version='1.0.0rc2')

parser = argparse.ArgumentParser(description='Generate an XML file from \
    a tree, an alignment and statistics.')
parser.add_argument('-t', '--tree', dest='treeFile', action='store',\
    required=True,\
    help='File containing a tree in Newick format')
parser.add_argument('-a', '--align', dest='alignmentFile', action='store',\
    required=True,\
    help='File containing an alignment in FASTA format')
parser.add_argument('-r', '--results', dest='resultsFile', action='store',\
    required=True,\
    help='File containing the results')
parser.add_argument('-s', '--sep', dest='sep', action='store',\
    required=False,\
    default='\t',\
    help='Column separator')
parser.add_argument('-c', '--col', dest='statcol', action='store', type=int,\
    default=1,\
    help='Index of the results column to use')
parser.add_argument('-n', '--nostat', dest='nostat', action='store', type=float,\
    default=-1.0,\
    help='Value to use in case there is no statistic associated\
    with a site in the sequence')
parser.add_argument('-b', '--branchsite', dest='isBranchsite', action='store_true',\
    required=False,\
    help='View site-branch data')
parser.add_argument('--skipmissing', dest='skipMissingSites', action='store_true',\
    required=False,\
    help='Prevent the addition of special values (-n, --nostat) for sites that are absent from the results file. \
        This results in sites being next to each other on the graph even though their positions are distant.')
parser.add_argument('--isnucleic', dest='isNucleic', action='store_true',\
    required=False,\
    help='Specify this argument if the sequences are not to be treated as DNA/RNA')
parser.add_argument('-o', '--output', dest='output', action='store',\
    help='Name of the output XML file (if not specified, the XML will have \
    the same name as the tree file)')
args = parser.parse_args()


def loadDico(fileDico):
    """
    Fonction qui prend un fichier d'alignement en entree et retourne un dictionnaire des noms d'espece des sequences
    """

    file = open(fileDico,"r")
    speciesDico = {}
    for line in file:
        if line[0]==">":
            speciesDico[line.split('>')[1].split('\n')[0]] = line.split('>')[1].split('\n')[0]
            # tline = re.split('_',line)
            # #key = f"{tline[0]} {tline[1]}"
            # key = line.split('\n')[0]
            # fin = tline[4].split("\n")[0]
            # speciesDico[key.split(">")[1]] = f"{tline[2]} {tline[3]} {fin}"
    file.close()
    return speciesDico


def nucToAmino(nuc_seq:str):
    '''Converts a DNA/RNA sequence into a proteic sequence.'''

    matches = {
        'AAA':'K', 'AAC':'N', 'AAG':'K', 'AAT':'N',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AGA':'R', 'AGC':'S', 'AGG':'R', 'AGT':'S',
        'ATA':'I', 'ATC':'I', 'ATG':'M', 'ATT':'I',
        'CAA':'Q', 'CAC':'H', 'CAG':'Q', 'CAT':'H',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'GAA':'E', 'GAC':'D', 'GAG':'E', 'GAT':'D',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'TAA':'*', 'TAC':'Y', 'TAG':'*', 'TAT':'Y',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TGA':'*', 'TGC':'C', 'TGG':'W', 'TGT':'C',
        'TTA':'L', 'TTC':'F', 'TTG':'L', 'TTT':'F',

        'AAU':'N',
        'ACU':'T',
        'AGU':'S',
        'AUA':'I', 'AUC':'I', 'AUG':'M', 'AUU':'I',
        'CAU':'H',
        'CCU':'P',
        'CGU':'R',
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'GAU':'D',
        'GCU':'A',
        'GGU':'G',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'UAA':'*', 'UAC':'Y', 'UAG':'*', 'UAU':'Y',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UGA':'*', 'UGC':'C', 'UGG':'W', 'UGU':'C',
        'UUA':'L', 'UUC':'F', 'UUG':'L', 'UUU':'F',

        '---':'-'
    }
    aa = ''
    codons = [nuc_seq[i:i+3].upper() for i in range(0, len(nuc_seq), 3)]
    for codon in codons:
        if len(codon) == 3:
            try:
                aa += matches[codon]
            except KeyError:
                print(f"Unknown codon: {codon}, adding 'X' to sequence")
                aa += 'X'
        else:
            print(f"Ignored: {codon} (not a codon)")
    return aa


def loadAlignment(alignmentFile):
    """Loads a FASTA alignment."""

    alignmentDict = {}
    maxSeqIdLength = 0
    with open(alignmentFile, 'r') as af:
        for line in af:
            if line[0] == '>': # sequence id
                seq_id = line.strip('\n')[1:]
                if len(seq_id) > maxSeqIdLength:
                    maxSeqIdLength = len(seq_id)
                alignmentDict[seq_id] = ''
            else: # sequence
                aligned_seq = line.strip('\n')
                if len(alignmentDict[seq_id]) == 0:
                    alignmentDict[seq_id] = aligned_seq
                else:
                    alignmentDict[seq_id] += aligned_seq
    return alignmentDict, maxSeqIdLength


def loadResultsSites(resultsFile, statcol=1, nostat_value=-1.0, sep='\t', skipMissingSites=False):
    """Loads site results from column with index <statcol>."""

    resultsDict = {}
    with open(resultsFile, 'r') as f:
        i = -1
        for line in f:
            line = line.strip('\n').split(sep)
            if re.search('^[0-9]+$', line[0]): # results line
                try:
                    site = int(line[0])
                    res = float(line[statcol])
                except ValueError:
                    print(f"Conversion failed in line {line}")
                else:
                    if i == -1:
                        i = site
                    while i < site: # in case there is no statistic for
                                    # a site, give it a default value
                        if not skipMissingSites:
                            print(f'Site {i} missing (current line: site {site})')
                            resultsDict[i] = nostat_value
                        else:
                            print(f'Site {i} skipped')
                        i += 1
                    resultsDict[i] = res
            else: # other line (e.g. header)
                # print(line)
                pass
            i += 1

    resultsList = []
    for key, item in resultsDict.items():
        resultsList.append(item)
    return resultsList


def loadResultsBranchSite(resultsFile, sep='\t', skipMissingSites=False):
    """Loads site-branch results."""

    d_cols = {}
    column_lists = []
    with open(resultsFile, 'r') as f:
        headers = f.readline().strip().split(sep)
        for header in headers:
            column_lists.append([header])

        for line in f:
            line = line.strip().split(sep)
            for i in range(len(line)):
                column_lists[i].append(line[i])
        
        # column_lists: [[sites, 1, 2, ...], [0, 0.1248, 0.12381, ...], [1, 0.131, 0.835, ...], ...]

        for column in column_lists:
            d_cols[column[0]] = column[1:]
        
        # d: {sites: [1, 2, ...], 0: [0.1248, 0.12381, ...], 1: [0.131, 0.835, ...], ...}
        
        position_header = 'sites'
        d_cols_2 = dict(d_cols)
        for col_key in d_cols:
            # if col_key != position_header:
            ## For every branch
            if re.search(r'^[0-9]+$', col_key):
                col_text = ''
                # print(f'd_cols[{col_key}]', d_cols[col_key])
                ## Add each result to the text
                for i in range(len(d_cols[position_header])):
                    col_text += f'{d_cols[col_key][i]}, '
                    # col_text: '0.1248, 0.12381, ...'
                ## Add brackets for JSON format
                col_text = '['+col_text[:-2]+']' # [:-2] to remove last space and comma
                d_cols_2[col_key] = col_text
                # d_cols_2: {1: '[0.1248, 0.12381, ...]', ...}
    return d_cols_2


def getColnames(file, sep='\t'):
    '''Returns a list of header items in a file.'''

    with open(file, 'r') as f:
        header_items =  f.readline().rstrip().split(sep)
    return header_items


# #
# tree = "((((((((papAnuXM_017956960:0.00809496,(((macFasXM_005550221:0.00289701,(macMulXM_015134241:0.0022655,macNemXM_011730830:0.000864565)4:0.00124679)5:0.0077718,manLeuXM_011998270:0.00501842)7:0.00250405,cerAtyXM_012032058:0.00439159)9:0.00131476)10:0.00588244,chlSabXM_007982155:0.013576)12:0.0102079,(colAngXM_011955057:0.0417556,(rhiRoxXM_010370424:0.00239969,rhiBieXM_017870301:0.0138669)16:0.044625)17:0.00385901)18:0.0333012,((((panTroXM_009453613:0.00851837,homSapCCDS34680:0.00463484)21:0.00545281,gorGorXM_004045741:0.00956036)23:0.0130972,ponAbeXM_002818211:0.0293612)25:0.00339537,nomLeuXM_012510254:0.0334299)27:0.0149917)28:0.124488,carSyrXM_008064267:0.286938)30:0.0253192,(otoGarXM_003782669:0.195123,(proCoqXM_012647381:0.044556,micMurXM_012779641:0.0980136)34:0.0569938)35:0.0394367)36:1.08999,panPanXM_008961997:0.0577899)38:0.0642909,aotNanXM_012450812:0.0367385,cebCapXM_017525097:0.0433883);"
# tree = '(((A,(B,C)),(D,E));'
def normalizeTree(tree:str):
    '''Adds branch numbers following a <name>:<number>:<length> syntax.'''

    # print(tree)
    tree = re.sub(r'([\),])([0-9]+):', r'\1:', tree)
    tree = re.sub(r'([\),])(:[0-9]+):', r'\1:', tree)
    # print(tree)
    # Tree without additional information other than branch lengths
    
    new_tree = ''
    branch_id = 0
    if ':' in tree:
        for i in range(len(tree)):
            if tree[i] in ':':
                new_tree += ':' + str(branch_id) + tree[i]
                # while re.match(r'[0-9\.:]', tree[i]):
                #     new_tree += tree[i]
                #     i += 1
                #  + str(branch_id) + tree[i]
                branch_id += 1
            else:
                new_tree += tree[i]
    else:
        for i in range(len(tree)):
            if tree[i] in ',)':
                new_tree += ':' + str(branch_id) + ':' + str(1) + tree[i]
                branch_id += 1
            else:
                new_tree += tree[i]
    return new_tree
# tree = normalizeTree(tree)
# print(tree)
#


def createPhyloXML(fam,newick):
    newick = normalizeTree(newick)
    # Parse and return exactly one tree from the given file or handle
    # if not ':' in newick:
    #     nv_arbre = ""
    #     for i in range(len(newick)):
    #         if (newick[i]==',' and newick[i-1]!=')') or (newick[i]==')' and newick[i-1]!=')'):
    #             nv_arbre+=":0.7"
    #             nv_arbre+=newick[i]
    #         elif (newick[i]==',' and newick[i-1]==')') or (newick[i]==')' and newick[i-1]==')'):
    #             nv_arbre+=":0.4"
    #             nv_arbre+=newick[i]
    #         else:
    #             nv_arbre+=newick[i]
    #     newick = nv_arbre

    # print(f'newick:\n{newick}')

    # Tree now has a <branch_name>:<number>:<length> syntax
    handle = StringIO(newick)
    # print('handle:', handle)
    trees = Phylo.read(handle, 'newick')
    # print('trees:', trees)
    # Clade(branch_length=0.0642909)

    # Write a sequence of Tree objects to the given file or handle
    rd = str(random.randint(0,1000))
    Phylo.write([trees], 'tmpfile-'+rd+'.xml', 'phyloxml')
    file = open('tmpfile-'+rd+'.xml', 'r')
    # Copie tous les objets dans une variable et supprime le fichier créé
    text = file.read()
    file.close()
    os.remove('tmpfile-'+rd+'.xml')
    #
    p = XMLParser(huge_tree=True)
    # text = text.replace("phy:", "")

    # text = re.sub("b'([^']*)'", "\\1", text)
    # text = re.sub('branch_length_attr="[^"]+"', "", text)
    header = "<phyloxml>"

    text = re.sub('<phyloxml[^>]+>', header, text)
    text = text.replace('Phyloxml', 'phyloxml')
    tree = etree.fromstring(text, parser=p)
    treename = etree.Element("name")
    treename.text = fam
    ins = tree.find('phylogeny')
    ins.append(treename)

    clade = tree.xpath("/phyloxml/phylogeny/clade")
    subtree = tree.xpath("/phyloxml")
    nbfeuille = 0
    famspecies = {}
    # branch_id = 0

    res_colnames = getColnames(args.resultsFile)[1:]
    # print('res_colnames:', res_colnames)
    colname_index = 0
    for element in clade[0].iter('clade'):
        # print(element.tag)
        # look for a <name> element in the current <clade> element
        enom = element.find('name')
        # print(enom)
        if (enom is not None):
            # if there is a <name> element, it means we're in a leaf
            nbfeuille = nbfeuille + 1
            cds = enom.text
            sp = dico.get(cds)
            if (not  sp):
                print ("undefined species for "+ cds)
                sp = "undefined"
            famspecies[sp] = 1

            ## Affectation de la séquence pour l'ID en cours
            seq_alg = alignmentDict.get(cds)
            if not seq_alg:
                print ("undefined alignment for "+ cds)
                seq_alg = ""

            evrec = etree.Element("eventsRec")
            # branches = etree.Element("branchStats")
            leaf = etree.Element("leaf")
            if 'crossdico' in globals():
                crossref = etree.Element("crossref")
                if cds in crossdico[0]:
                    response = crossdico[0][cds]
                    tabbuf = response.split("|")
                    print (tabbuf)
                    for buf in tabbuf:
                        print ("process "+buf)
                        tabcross = buf.split(":")
                        if len(tabcross) > 1 :
                            crossref.set(tabcross[0], tabcross[1])
            leaf.set('speciesLocation', sp)
            if 'seqdefdico' in globals():
                if cds in seqdefdico:
                    leaf.set('defintiion', seqdefdico[cds])

            ## Ajout des séquences aux feuilles
            if args.isNucleic:
                leaf.set('dnaAlign', seq_alg) # ajout de la séquence en nucléotides
            # leaf.set('aaAlign', translate.dna_to_prot(seq_alg)) # ajout de la séquence en acides aminés
            # leaf.set('aaAlign', dna_to_prot(seq_alg)) # ajout de la séquence en acides aminés
            # print('args.isNucleic', args.isNucleic)
            if args.isNucleic:
                leaf.set('aaAlign', nucToAmino(seq_alg)) # ajout de la séquence traduite
            else:
                leaf.set('aaAlign', seq_alg) # ajout de la séquence brute

            if 'crossdico' in globals():
                leaf.append(crossref)
            evrec.append(leaf)
            element.append(evrec)
        
        if args.isBranchsite:
            if element.find('branch_length') is not None:
                branch_id = res_colnames[colname_index]
                print('branch_id', branch_id)
                branch_info = etree.Element('branch_info')
                branch_info.set('id', str(branch_id))
                branch_info.set('results', str(dict_results[str(branch_id)]))
                print(str(branch_id), dict_results[str(branch_id)][:10])
                element.append(branch_info)
                colname_index += 1
                # branch_id += 1
    
    print ("Number of leaves : ")
    print (nbfeuille)
    nbspecies = len(famspecies)
    print ("Number of species : ")
    print (nbspecies)

    ## Ajout des résultats
    globalResultsElement = etree.Element('global_results')
    # globalResultsElement.set('results', resultsText)
    globalResultsElement.set('results', str(resultsList))
    # globalResultsElement.text = resultsText

    LengthMaxSeqID = etree.Element('maxSeqIdLength')
    LengthMaxSeqID.text = str(maxSeqIdLength)

    treesize =  etree.Element("size")
    treesize.set('leaves',str(nbfeuille))
    treesize.set('species',str(nbspecies))
    e=subtree[0].find('phylogeny')
    e.append(treesize)
    e.append(LengthMaxSeqID)
    e.append(globalResultsElement) # ajout de la balise contenant les résultats
    text =  minidom.parseString(ElementTree.tostring(subtree[0])).toprettyxml()
    # remove blank lines
    cleantext = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    return cleantext


sys.setrecursionlimit(15000)
# print(sys.getrecursionlimit())

print ("Loading alignment... ")
loadedAlignment = loadAlignment(args.alignmentFile)
alignmentDict, maxSeqIdLength = loadedAlignment[0], loadedAlignment[1]
print ("OK")

print ("Loading results... ")
# resultsText =  loadResultsSites(args.resultsFile, args.statcol, args.nostat, sep=args.sep)
resultsList =  loadResultsSites(args.resultsFile, args.statcol, args.nostat, sep=args.sep, skipMissingSites=args.skipMissingSites)
if args.isBranchsite:
    dict_results = loadResultsBranchSite(args.resultsFile, sep=args.sep)
print("OK")

#Creates empty phyloxml document
# project = Phyloxml()   # a decommenter si on veut un fichier xml unique

# Loads Species name dico
dico = loadDico(args.alignmentFile)

# Loads newick tree
treefile = open(args.treeFile, "r")
if args.output:
    output_name = args.output
else:
    if '.' in args.treeFile:
        output_name = args.treeFile[::-1].split('.', 1)[1][::-1]
    else:
        output_name = args.treeFile
xmloutputfile = open(output_name,"w")

for line in treefile:
    tline = re.split(' ',line)
    if len(tline) > 1:
        newick=tline[1]
        fam=tline[0]
    else:
        newick = tline[0]
        fam = ''
    phyloxmltree = createPhyloXML(fam,newick)
    xmloutputfile.write(phyloxmltree)
    print("Famille "+fam+" OK")

treefile.close()
xmloutputfile.close()
