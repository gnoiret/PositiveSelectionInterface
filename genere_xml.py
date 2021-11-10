#
# Part of this  code is taken from https://groups.google.com/forum/#!topic/etetoolkit/cYTHHsL21KY
# written by Jaime Huerta-Cepas

"""Ecrit un  arbre au format XML .
Usage:
  genere_xml.py <treeFile> <alignmentFile> <resultsFile>

Positional arguments:
  treeFile              family name / phylogenic trees in newick format
  alignmentFile         multiple alignment in fasta format
  resultsFile           statistics

"""
import sys
import re
import random
import os
from Bio import Phylo
from io import StringIO
# from cStringIO import StringIO
import time
from ete3 import Phyloxml, phyloxml

from lxml import etree
from xml.etree import ElementTree
from xml.dom import minidom

from lxml.etree import XMLParser, parse

from docopt import docopt
import sqlite3
import zlib
import base64

# import file_reader
# import translate

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

def loadAlignment(alignmentFile):
    alignmentDict = {}
    
    with open(alignmentFile, 'r') as af:
        for line in af:
            # if len(line) > 50:
            #   print('line:', line[:50] + ' ...')
            # else:
            #   print('line:', line)
            if line[0] == '>': # la ligne est un en-tête fasta
                seq_id = line.strip('\n')[1:]
                # print('seq_id:', seq_id)
                alignmentDict[seq_id] = ''
            else: # la ligne est une séquence alignée
                aligned_seq = line.strip('\n')
                # print('aligned_seq:', aligned_seq)
                alignmentDict[seq_id] = aligned_seq

    # print(alignmentDict)
    #alignmentDict: {'XM_023507720dot1_oto_Gar_SAMD9': 'ATGGCAAAGCA(...)', (...)}
    return alignmentDict

def loadResults(resultsFile):
    resultsDict = {}
    with open(resultsFile, 'r') as f:
        i = 0
        for line in f:
            if i > 0:   # on évite de lire les en-têtes des colonnes
                line = line.strip('\n').split('\t')
                try:
                    site = int(line[0])
                    res = float(line[8])
                except ValueError:
                    print('Conversion failed:', line[0], line[8])
                else:
                    while not i == site:    # si le site est absent, on lui définit une statistique aberrante
                        print(f'Site {i} missing')
                        resultsDict[i] = -1.1111
                        i += 1
                    resultsDict[i] = res
                    # print(site == i, site, i, res)
            i += 1

    resultsText = ''
    for key, item in resultsDict.items():
        # print(f'{key} : {item}')
        resultsText += f'{key}:{item}'
        if key != max(resultsDict.keys()):
            resultsText += ' '
    # print(f'>{resultsText}<')
    return resultsText

def createPhyloXML(fam,newick):
    #Parse and return exactly one tree from the given file or handle
    if not ':' in newick:
        nv_arbre = ""
        for i in range(len(newick)):
            if (newick[i]==',' and newick[i-1]!=')') or (newick[i]==')' and newick[i-1]!=')'):
                nv_arbre+=":1"
                nv_arbre+=newick[i]
            elif (newick[i]==',' and newick[i-1]==')') or (newick[i]==')' and newick[i-1]==')'):
                nv_arbre+="50:0.4"
                nv_arbre+=newick[i]
            else:
                nv_arbre+=newick[i]
        newick = nv_arbre
    # print(newick)
    handle = StringIO(newick)
    trees = Phylo.read(handle, 'newick')
    #Write a sequence of Tree objects to the given file or handle
    rd = str(random.randint(0,1000))
    Phylo.write([trees], 'tmpfile-'+rd+'.xml', 'phyloxml')
    file = open('tmpfile-'+rd+'.xml', 'r')
    #Copie tous les objets dans une variable et supprime le fichier créé
    text = file.read()
    file.close()
    os.remove('tmpfile-'+rd+'.xml')
    #
    p = XMLParser(huge_tree=True)
    text = text.replace("phy:", "")

    text = re.sub("b'([^']*)'", "\\1", text)
    text = re.sub('branch_length_attr="[^"]+"', "", text)
    header = "<phyloxml>"

    text = re.sub('<phyloxml[^>]+>', header, text)
    text = text.replace('Phyloxml', 'phyloxml')
    tree = etree.fromstring(text,parser=p)
    # ajout du nom d'arbre
    treename = etree.Element("name")
    treename.text = fam
    ins = tree.find('phylogeny')
    ins.append(treename)

    clade = tree.xpath("/phyloxml/phylogeny/clade")
    subtree = tree.xpath("/phyloxml")
    nbfeuille = 0
    famspecies = {}

    for element in clade[0].iter('clade'): # pour chaque id de séquence
        enom=element.find('name')
        if (enom is not None) :
            nbfeuille = nbfeuille + 1
            cds = enom.text
            # sp = dico.get(cds)
            # if (not  sp):
            #     print ("undefined species for "+ cds)
            #     sp = "undefined"
            # famspecies[sp] = 1

            ## Affectation de la séquence pour l'ID en cours
            seq_alg = alignmentDict.get(cds)
            if not seq_alg:
                print ("undefined alignment for "+ cds)
                seq_alg = ""

            # synLeft=synteLeftDico.get(cds)
            # if (not synLeft):
            #     synLeft = ""
            # synRight=synteRightDico.get(cds)
            # if (not synRight):
            #     synRight = ""
            
            # seq = dico_sequences.get(cds)
            # if not seq:
            #     seq = ""

            evrec = etree.Element("eventsRec")
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
            # leaf.set('speciesLocation', sp)
            if 'seqdefdico' in globals():
                if cds in seqdefdico:
                    leaf.set('defintiion', seqdefdico[cds])

            # leaf.set('syntenyLeft', synLeft)
            # leaf.set('syntenyRight', synRight)

            ## Ajout des séquences aux feuilles
            leaf.set('dnaAlign', seq_alg) # ajout de la séquence en nucléotides
            # leaf.set('aaAlign', translate.dna_to_prot(seq_alg)) # ajout de la séquence en acides aminés
            leaf.set('aaAlign', dna_to_prot(seq_alg)) # ajout de la séquence en acides aminés

            if 'crossdico' in globals():
                leaf.append(crossref)
            evrec.append(leaf)
            element.append(evrec)
    print ("Number of leaves : ")
    print (nbfeuille)
    nbspecies = len(famspecies)
    print ("Number of species : ")
    print (nbspecies)

    ## Ajout des résultats
    # resultsText = ''
    # for result in resultsList:
    #     resultsText += str(result) + ' '
    # resultsText = resultsText.strip()
    # print(resultsText)
    resultsElement = etree.Element('statistics')
    resultsElement.set('results', resultsText)

    treesize =  etree.Element("size")
    treesize.set('leaves',str(nbfeuille))
    treesize.set('species',str(nbspecies))
    e=subtree[0].find('phylogeny')
    e.append(treesize)
    e.append(resultsElement) # ajout de la balise contenant les résultats
    text =  minidom.parseString(ElementTree.tostring(subtree[0])).toprettyxml()
    # remove blank lines
    cleantext = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    return cleantext


args = docopt(__doc__)

tree = args["<treeFile>"]
# speciesDico = args["<speciesDicoFile>"]
# synLeft = args["<syntenyLeftFile>"]
# synRight = args["<syntenyRightFile>"]
alignment = args["<alignmentFile>"]
results = args["<resultsFile>"]
arguments = docopt(__doc__, version='1.0.0rc2')

sys.setrecursionlimit(15000)
print(sys.getrecursionlimit())

# print ("Loading species...")
# dico = loadDico(speciesDico)
# print ("OK")

# print ("Loading synteny left... ")
# synteLeftDico =  loadSynte(synLeft)
# print ("OK")

# print ("Loading synteny right... ")
# synteRightDico =  loadSynte(synRight)
# print ("OK")

print ("Loading alignment... ")
# alignmentDict =  file_reader.loadAlignment(alignment)
alignmentDict =  loadAlignment(alignment)
print ("OK")

print ("Loading results... ")
# resultsText =  file_reader.loadResults(results)
resultsText =  loadResults(results)
print ("OK")

#Creates empty phyloxml document
#project = Phyloxml()   a decommenter si on veut un fichier xml unique

# Loads newick tree
treefile = open(tree,"r")
xmlouputfile = open(tree+".xml","w")


for line in treefile:
    tline = re.split(' ',line)
    # print('tline:', tline)
    if len(tline) > 1:
        newick=tline[1]
        fam=tline[0]
    else:
        newick = tline[0]
        fam = ''
    phyloxmltree = createPhyloXML(fam,newick)
    xmlouputfile.write(phyloxmltree)
    print ("Famille "+fam+" OK")

treefile.close()
xmlouputfile.close()
