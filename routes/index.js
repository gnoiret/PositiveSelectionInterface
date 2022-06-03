const upload_dir = 'uploads/';
const xml_dir = 'uploads/';

const bodyParser = require('body-parser');
// const browser = require('browser-detect');
const express = require('express');
const router = express.Router();
// const formidable = require('formidable');
const fs = require('fs');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
// const path = require('path');
const url = require('url');
// const util = require('util');

const {exec} = require('child_process');
router.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
router.use(bodyParser.json()); // support json encoded bodies
if (typeof localStorage === "undefined" || localStorage === null) {
  var LocalStorage = require('node-localstorage').LocalStorage;
  localStorage = new LocalStorage('./scratch');
}

// const upload = multer({
//   storage: multer.diskStorage({
//     destination: (req, file, callback) => {
//       var type = req.params.type;
//       var path = `./uploads/${type}`;
//       fs.mkdirsSync(path);
//       callback(null, path);
//     },
//     filename: (req, file, callback) => {
//       //originalname is the uploaded file's name with extn
//       callback(null, file.originalname);
//     }
//   })
// });

// Home
// ----
router.get('/', function(req, res) {
  res.render('index.ejs', {title: 'M1 Internship : Positive Selection Interface'});
});

// POST upload_files
// -----------
router.post("/upload_files", upload.fields([
  {name: 'file_t', maxCount: 1}, 
  {name: 'file_a', maxCount: 1}, 
  {name: 'file_r', maxCount: 1}
]), 
(req, res) => {
  console.log('Successfully uploaded files');
  console.log(req.body);
  console.log(req.files);
  
  var currentTimestampMs = Date.now();
  // var fname_t = req.files.file_t[0].filename;
  // var fname_a = req.files.file_a[0].filename;
  // var fname_r = req.files.file_r[0].filename;
  var fname_t = currentTimestampMs+'-t'+req.files.file_t[0].filename.substring(0, 3);
  var fname_a = currentTimestampMs+'-a'+req.files.file_a[0].filename.substring(0, 3);
  var fname_r = currentTimestampMs+'-r'+req.files.file_r[0].filename.substring(0, 3);
  fs.rename(req.files.file_t[0].path, upload_dir+fname_t, function(err) {
    if (err) {
      console.log('ERROR:', err);
    }
  });
  fs.rename(req.files.file_a[0].path, upload_dir+fname_a, function(err) {
    if (err) {
      console.log('ERROR:', err);
    }
  });
  fs.rename(req.files.file_r[0].path, upload_dir+fname_r, function(err) {
    if (err) {
      console.log('ERROR:', err);
    }
  });
  // req.files.forEach(file => fs.rename(file[0].path, file[0].destination+Date.now()+'-'+file[0].filename.substring(0, 3), function(err) {
  //   if (err) {
  //     console.log('ERROR:', err);
  //   }
  // }));
  // Date.now() is the current timestamp in milliseconds
  var fname_xml = currentTimestampMs
    // +'-xml-'
    + fname_t.split('-')[1]
    + fname_a.split('-')[1]
    + fname_r.split('-')[1]
    // +'.xml'
    ;
    // + fname_t.substring(0, 3)
    // + fname_a.substring(0, 3)
    // + fname_r.substring(0, 3)+'.xml';
  const full_path_xml = xml_dir + fname_xml;
  const statcol = req.body.statcol;
  const nostat = req.body.nostat;
  var branchSite = req.body.branchSite;
  var logBranchLength = req.body.logBranchLength;
  var skipMissingSites = req.body.skipMissingSites;

  console.log('branchSite:', branchSite);
  if (branchSite != undefined) {
    console.log('branchSite');
    branchSite = true;
  } else {
    console.log('not branchSite');
    branchSite = false;
  }
  console.log('logBranchLength:', logBranchLength);
  if (logBranchLength != undefined) {
    console.log('logBranchLength');
    logBranchLength = true;
  } else {
    console.log('not logBranchLength');
    logBranchLength = false;
  }
  console.log('skipMissingSites:', skipMissingSites);
  if (skipMissingSites != undefined) {
    console.log('skipMissingSites');
    skipMissingSites = true;
  } else {
    console.log('not skipMissingSites');
    skipMissingSites = false;
  }

  // console.log('Tree: ' + fname_t + '\n' +
  // 'Alignment: ' + fname_a + '\n' +
  // 'Results: ' + fname_r + '\n' +
  // 'XML: ' + fname_xml);

  // console.log(req.files);
  // console.log('req.files.length: '+req.files.length);

  // Faire tourner genere_xml.py avec exec()
  console.log('Generating XML tree');
  exec('python3 genere_xml.py'
      +' -t '+upload_dir+fname_t
      +' -a '+upload_dir+fname_a
      +' -r '+upload_dir+fname_r
      +' -o '+xml_dir+fname_xml
      +' -c '+statcol
      +' -n '+nostat
      +(branchSite?' -b ':'')
      +(skipMissingSites?' --skipmissing ':''),
  (error, stdout, stderr) => {
    if (error) {
      console.log(`error: ${error.message}`);
    } else {
      console.log('Deleting data files');
      exec('rm'
        +' '+upload_dir+fname_t
        +' '+upload_dir+fname_a
        +' '+upload_dir+fname_r,
        (error, stdout, stderr) => {
          if (error) {
            console.log(`error: ${error.message}`);
          }
          if (stderr) {
            console.log(`error: ${stderr}`);
          }
          console.log(`${stdout}`);
        }
      )
    }
    if (stderr) {
      console.log(`error: ${stderr}`);
    }
    console.log(`${stdout}`);
    
    // Lire l'arbre XML en JSON et afficher les données
    const fname = full_path_xml;
    fs.readFile(fname, 'utf8' , (err, data) => {
      if (err) {
        res.render('error.ejs', {message:"Erreur de lecture",error:err});
      }
      var xml_digester = require("xml-digester");
      var handler = new xml_digester.OrderedElementsHandler("eventType");
      var options = {
        "handler": [{
          "path": "eventsRec/*",
          "handler": handler
        }]
      };
      var digester = xml_digester.XmlDigester(options);
      digester.digest(data, function(err, results) {
        if (err) {
          console.log(err);
          return;
        }
        var JSONtree = JSON.stringify(results);
        var JSONpattern = JSON.stringify("0:homSapCCDS34680"); // Séquence à mettre en valeur
        console.log('Rendering view');
        res.render('displaytree.ejs', {arbre:JSONtree, pattern:JSONpattern, branchSite:branchSite, logBranchLength:logBranchLength});

        console.log('Deleting XML file');
        exec('rm'
          +' '+xml_dir+fname_xml,
          (error, stdout, stderr) => {
            if (error) {
              console.log(`error: ${error.message}`);
            }
            if (stderr) {
              console.log(`error: ${stderr}`);
            }
            console.log(`${stdout}`);
          }
        )
      });
    });
  });
});

// GET test-formulaire
// -----------
router.get('/test-formulaire', function(req, res, next) {
  var pathname = url.parse(req.url).pathname;
  console.log('Accès à ' + pathname);
  res.render('test-formulaire.ejs');
});

// GET test-arbre
// -----------
router.get('/test-arbre', function(req, res, next) {
  var pathname = url.parse(req.url).pathname;
  console.log('Accès à ' + pathname);
  res.render('test-arbre.ejs');
});

// // GET display
// // -----------
// router.get('/display', function(req, res, next) {
//   console.log('Accès à /display');
//   const fs = require('fs');
//   fs.readFile('input_tree.xml', 'utf8' , (err, data) => {
//     if (err) {
//       res.render('error.ejs', {message:"Erreur de lecture",error:err});
//     }
//     var xml_digester = require("xml-digester");
//     var handler = new xml_digester.OrderedElementsHandler("eventType");
//     var options = {
//       "handler": [{
//         "path": "eventsRec/*",
//         "handler": handler
//       }]
//     };
//     var digester = xml_digester.XmlDigester(options);
//     digester.digest(data, function(err, results) {
//       if (err) {
//         console.log(err);
//         return;
//       }
//       var JSONtree = JSON.stringify(results);
//       // Séquence à mettre en valeur :
//       var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
//       res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
//     });
//   });
// });
// // POST display
// // ------------
// router.post('/display', upload.single('file'), function(req, res, next) {
//   console.log('Accès à /display');
//   const fs = require('fs');
//   const fname = 'uploads/' + req.file.filename
//   fs.readFile(fname, 'utf8' , (err, data) => {
//     if (err) {
//       res.render('error.ejs', {message:"Erreur de lecture",error:err});
//     }
//     var xml_digester = require("xml-digester");
//     var handler = new xml_digester.OrderedElementsHandler("eventType");
//     var options = {
//       "handler": [{
//         "path": "eventsRec/*",
//         "handler": handler
//       }]
//     };
//     var digester = xml_digester.XmlDigester(options);
//     digester.digest(data, function(err, results) {
//       if (err) {
//         console.log(err);
//         return;
//       }
//       var JSONtree = JSON.stringify(results);
//       // console.log(JSONtree);
//       // Séquence à mettre en valeur :
//       var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
//       res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
//     });
//   });
// });
// router.post('/display', upload.single('file'), function(req, res) {
//   console.log('Accès à /display');
//   const fs = require('fs');
//   const fname = 'uploads/' + req.file.filename
//   fs.readFile(fname, 'utf8' , (err, data) => {
//     if (err) {
//       res.render('error.ejs', {message:"Erreur de lecture",error:err});
//     }
//     var xml_digester = require("xml-digester");
//     var handler = new xml_digester.OrderedElementsHandler("eventType");
//     var options = {
//       "handler": [{
//         "path": "eventsRec/*",
//         "handler": handler
//       }]
//     };
//     var digester = xml_digester.XmlDigester(options);
//     digester.digest(data, function(err, results) {
//       if (err) {
//         console.log(err);
//         return;
//       }
//       var JSONtree = JSON.stringify(results);
//       // Séquence à mettre en valeur :
//       var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
//       res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
//     });
//   });
// });

// router.post("/upload_files", upload.fields('files'), (req, res) => {
//   console.log(req.body);
//   console.log(req.files);
//   if (req.files.length === 3) {
//     console.log("J'ai reçu exactement 3 fichiers ! ("+req.files.length+")");
//   } else {
//     console.log("Je n'ai pas reçu 3 fichiers. ("+req.files.length+")");
//     var err = "Wrong file amount";
//     throw err;
//   }
//   // res.json({ message: "Successfully uploaded files" });
//   // res.render('test1.ejs');
//   res.redirect('/test-formulaire');
// });
// function uploadFiles {
//   console.log(req.body);
//   console.log(req.files);
//   res.json({ message: "Successfully uploaded files" });
// }

// POST submit-test
// -----------
// router.post('/submit-test', function(req, res) {
//   var pathname = url.parse(req.url).pathname;
//   console.log('Accès à ' + pathname);
  // console.log(req, res);
  // console.log('texte : '+req.body.texte);
  // new formidable.IncomingForm().parse(req)
  // .on('error', (err) => {
  //   console.log('Error', err);
  //   throw err;
  // })
  // .on('aborted', () => {
  //   console.log('File upload aborted by the user');
  // })
  // .on('field', (name, field) => {
  //   console.log('Field', name, field);
  // })
  // .on('fileBegin', (name, file) => {
  //   console.log('Old path:', file.path);
  //   file.name = 'upload-' + file.name;
  //   file.path = __dirname + '/uploads/' + file.name;
  //   console.log('New name:', file.name);
  //   console.log('New path:', file.path);
  // })
  // .on('file', (name, file) => {
  //   // console.log('File', name, file);
  //   console.log('File', file.name, 'received, here is some information about it:');
  //   console.log('Size:', file.size, 'bytes');
  //   console.log('Type:', file.type);
  //   console.log('Path:', file.path)
  // })
  // .on('end', () => {
  //   res.end();
  // });
// });

// const fs = require('fs');
// // var mavar = JSON.parse('[[1,0.2],[2,0.33],[3,1.0]]');
// // var stat_results = JSON.stringify('1:0.2 2:0.33 3:1.0 4:0.33 5:0.2');
// fs.readFile('routes/uploads/upload-fichier-test-formulaire.txt', 'utf8', (err, data) => {
//   if (err) {
//     console.log('Error:', err);
//     return;
//   }
//   console.log('Data: ', data);
//   // if (data) {
//   //   var stat_results = JSON.stringify(data);
//   //   console.log('--------- Results: ' + stat_results);
//   //   res.render('test_affichage_fichier.ejs', {resultats:stat_results});
//   // }
// });

// GET test-affichage
// -----------
// router.get('/test-affichage-graphe', function(req, res, next) {
//   var pathname = url.parse(req.url).pathname;
//   console.log('Accès à ' + pathname);
//   res.render('test_affichage_graphe.ejs');
// });

// GET test-affichage-fichier
// -----------
// router.get('/test-affichage-fichier', function(req, res, next) {
//   var pathname = url.parse(req.url).pathname;
//   console.log('Accès à ' + pathname);

//   fs.readFile('input_tree.xml', 'utf8' , (err, data) => {
//     if (err) {
//       res.render('error.ejs', {message:"Erreur de lecture",error:err});
//     }
//     var xml_digester = require("xml-digester");
//     var handler = new xml_digester.OrderedElementsHandler("eventType");
//     var options = {
//       "handler": [{
//         "path": "eventsRec/*",
//         "handler": handler
//       }]
//     };
//     var digester = xml_digester.XmlDigester(options);
//     digester.digest(data, function(err, results) {
//       if (err) {
//         console.log(err);
//         return
//       }
//       var JSONtree = JSON.stringify(results);
//       // Séquence à mettre en valeur :
//       var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
//       res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
//     });
//   });

// GET taxodico
// ------------
// router.get('/taxodico', function(req, res, next) {
//   console.log('Accès à /taxodico');
//   res.render('gettaxojson.ejs', {species:JSON.stringify([]),colour:JSON.stringify([])});
// });

module.exports = router;
