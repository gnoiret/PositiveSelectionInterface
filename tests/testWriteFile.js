const fs = require('fs');
const file = fs.createWriteStream('file.txt');

for (let i = 0; i < 42; i++) {
    file.write('Hello world ' + i + '\n');
}
file.end();
