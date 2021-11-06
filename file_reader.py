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

def loadResults_old(resultsFile):
    resultsLst = []
    i = 0
    with open(resultsFile, 'r') as rf:
        for line in rf:
            if i > 0:
                res = line.strip('\n').split('\t')[8] # à faire : choix de la statistique
                # print(res)
                try:
                    res = float(res)
                    resultsLst.append(res)
                except ValueError:
                    print('not a float:', res)
            else:
                i += 1

    # print(f'début des {len(resultsLst)} résultats:', resultsLst[:3])
    # print(f'fin des {len(resultsLst)} résultats:', resultsLst[-3:])
    return resultsLst
