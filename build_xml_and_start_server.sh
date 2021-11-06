# pip3 install Bio ete3 lxml docopt
python genere_xml.py data/Ex_Arbre-SAMD9pri_MuscleCo_clado.tree data/Ex_Alignement-SAMD9pri_MuscleCo.fasta data/Ex_Resultats-SAMD9pri_M2.info || python3 genere_xml.py data/Ex_Arbre-SAMD9pri_MuscleCo_clado.tree data/Ex_Alignement-SAMD9pri_MuscleCo.fasta data/Ex_Resultats-SAMD9pri_M2.info;
cp data/Ex_Arbre-SAMD9pri_MuscleCo_clado.tree.xml input_tree.xml;
npm start;