// Plus adapté pour les gros traitements car utilise des flux, donc pas de stockage mémoire

const {spawn} = require('child_process');

const ls = spawn('ls', ['-la']);

ls.stdout.on('data', data => {
    console.log(`stdout: ${data}`);
});

ls.stderr.on('data', data => {
    console.log(`stderr: ${data}`);
});

ls.on('error', (error) => {
    console.log(`error: ${error.message}`);
});

ls.on('close', code => {
    console.log(`child process exited with code ${code}`);
});
