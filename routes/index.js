const upload_dir = 'uploads/';
const xml_dir = 'uploads/';

const bodyParser = require('body-parser');
// const browser = require('browser-detect');
const {exec} = require('child_process');
const express = require('express');
const router = express.Router();
// const formidable = require('formidable');
const fs = require('fs');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
// const path = require('path');
const url = require('url');
// const util = require('util');

router.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
router.use(bodyParser.json()); // support json encoded bodies
if (typeof localStorage === "undefined" || localStorage === null) {
  var LocalStorage = require('node-localstorage').LocalStorage;
  localStorage = new LocalStorage('./scratch');
}

// Home
// ----
router.get('/', function(req, res) {
  res.render('index.ejs', {title: 'M1 Internship : Positive Selection Interface'});
});

// POST upload_files
// -----------
router.post("/upload_files", upload.fields([
  {name: 'file_t'}, 
  {name: 'file_a'}, 
  {name: 'file_r'}
]), 
(req, res) => {
  console.log('Successfully uploaded files');
  console.log(req.body);
  console.log(req.files);
  
  var currentTimestampMs = Date.now();
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
  // Date.now() is the current timestamp in milliseconds
  var fname_xml = currentTimestampMs
    // +'-xml-'
    + fname_t.split('-')[1]
    + fname_a.split('-')[1]
    + fname_r.split('-')[1]
    // +'.xml'
    ;
  var full_path_xml = xml_dir + fname_xml;
  var statcol = req.body.statcol;
  var nostat = req.body.nostat;
  var resultsType = req.body.resultsType;
  var branchSite;
  var logBranchLength = req.body.logBranchLength;
  var skipMissingSites = req.body.skipMissingSites;
  var isNuc = req.body.isNuc;

  console.log('branchSiteMode ?', resultsType == 'branchSiteMode');

  console.log('branchSite:', branchSite);
  if (resultsType == 'branchSiteMode') {
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

  console.log('isNuc:', isNuc);
  if (isNuc != undefined) {
    console.log('isNuc');
    isNuc = true;
  } else {
    console.log('not isNuc');
    isNuc = false;
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
      +(skipMissingSites?' --skipmissing ':'')
      +(isNuc?' --isnucleic ':''),
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
        res.render('displaytree.ejs',
          {arbre:JSONtree, pattern:JSONpattern, branchSite:branchSite,
            logBranchLength:logBranchLength, isNuc:isNuc});

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

// GET taxodico
// ------------
// router.get('/taxodico', function(req, res, next) {
//   console.log('Accès à /taxodico');
//   res.render('gettaxojson.ejs', {species:JSON.stringify([]),colour:JSON.stringify([])});
// });

module.exports = router;
