const fs = require('fs');

fs.readFile('tests/file.txt', 'utf8' , (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(data);
});

// Ajout du fichier sur la page
  // Formulaire
// Clic sur le bouton "display"
  // Téléversement des fichiers dans le dossier uploads/ -> avec quels noms ?
  // tree_xxx.tree
  // alignment_xxx.fasta
  // results_xxx.info

  // fs.rename('before.json', 'after.json', err => {
  //     if (err) {
  //       return console.error(err)
  //     }
    
  //     //done
  //   })
//
// Exécution du script Python
  // spawn
  // python3 genere_xml.py -t tree_xxx.tree -a alignment_xxx.fasta -s results_xxx.info -c statcol -n nostat -o input_tree_xxx.xml
// Lecture de l'arbre XML
  // fs.readFile('tests/file.txt', 'utf8' , (err, data) => {
  //     if (err) {
  //     console.error(err)
  //     return
  //     }
  //     console.log(data)
  // })
//
// module path
