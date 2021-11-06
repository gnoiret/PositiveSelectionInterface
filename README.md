# Projet S1

Projet : développement d'une interface web pour la sélection positive

## Installation

### Prérequis

- [Python](https://www.python.org/downloads/) ainsi que les paquets suivants :
	- Bio
	- ete3
	- lxml
	- docopt
		    pip3 install Bio ete3 lxml docopt
- [Node.js](https://nodejs.org/fr/)

### Cloner le dépôt

`git clone https://github.com/gnoiret/Projet_S1.git`

## Utilisation

Le script `example.sh` construira l'arbre XML correspondant aux données fournies.

### Générer l'arbre à partir de l'exemple

`python3 genere_xml.py data/tree_example.tree data/alignment_example.fasta data/results_example.info`
`cp data/tree_example.tree.xml input_tree.xml`

### Lancer le serveur

`npm start`

Par défaut, l'interface sera accessible à l'adresse [http://localhost:8888/](http://localhost:8888/), définie dans le fichier `selpos.js` :

```
const PORT = 8888;
const HOST = '127.0.0.1';
```
