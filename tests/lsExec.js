const {exec} = require('child_process');

exec('ls -la', (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
    }
    if (stderr) {
        console.log(`error: ${stderr}`);
    }
    console.log(`${stdout}`);
});
