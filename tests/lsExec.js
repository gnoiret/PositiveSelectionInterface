const {exec} = require('child_process');

fname_xml = fname_tree.substring(0, 11) + fname_tree.substring(0, 11) + fname_tree.substring(0, 11)+'.xml';
exec('python3 genere_xml.py -t '+fname_tree+' -a '+fname_alignment+' -s '+fname_tree+' -o '+fname_xml+' -c '+statcol+' -n '+nostat,
(error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
    }
    if (stderr) {
        console.log(`error: ${stderr}`);
    }
    // console.log(`${stdout}`);// Récupérer l'arbre XML

});

// exec('ls -la', (error, stdout, stderr) => {
//     if (error) {
//         console.log(`error: ${error.message}`);
//     }
//     if (stderr) {
//         console.log(`error: ${stderr}`);
//     }
//     console.log(`${stdout}`);
// });

