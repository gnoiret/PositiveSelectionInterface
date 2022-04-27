const express = require('express');
const router = express.Router();
const formidable = require('formidable');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const util = require('util');
const url = require('url');
const path = require('path');
const browser = require('browser-detect');
const bodyParser = require('body-parser');
router.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
router.use(bodyParser.json()); // support json encoded bodies
if (typeof localStorage === "undefined" || localStorage === null) {
  var LocalStorage = require('node-localstorage').LocalStorage;
  localStorage = new LocalStorage('./scratch');
}

// var upload = multer({
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
router.get('/', function(req, res, next) {
  res.render('index.ejs', {title: 'M1 Internship : Positive Selection Interface'});
});

// GET display
// -----------
router.get('/display', function(req, res, next) {
  console.log('Accès à /display');
  const fs = require('fs');
  fs.readFile('input_tree.xml', 'utf8' , (err, data) => {
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
      // Séquence à mettre en valeur :
      var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
      res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
    });
  });
});
// POST display
// ------------
router.post('/display', upload.single('file'), function(req, res, next) {
  console.log('Accès à /display');
  const fs = require('fs');
  const fname = 'uploads/' + req.file.filename
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
      // Séquence à mettre en valeur :
      var JSONpattern = JSON.stringify("0:NM_001193307dot1_hom_Sap_SAMD9");
      res.render('displaytree.ejs', {arbre:JSONtree,pattern:JSONpattern});
    });
  });
});

// GET test-formulaire
// -----------
router.get('/test-formulaire', function(req, res, next) {
  var pathname = url.parse(req.url).pathname;
  console.log('Accès à ' + pathname);
  res.render('test1.ejs');
});

// POST upload_files
// -----------
// router.post("/upload_files", upload.array(['file_tree', 'file_alignment', 'file_results']), uploadFiles);
router.post("/upload_files", upload.array('files'), (req, res) => {
  console.log('coucou');
  console.log('req.body');  
  console.log('req.files');
  res.json({ message: "Successfully uploaded files" });
});
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
