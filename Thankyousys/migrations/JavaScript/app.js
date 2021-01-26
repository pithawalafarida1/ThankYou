const dialogflow = require("@google-cloud/dialogflow");
const uuid = require("uuid");
const express = require("express");
const bodyParser = require("body-parser");

const path = require('path');
const crypto = require('crypto');
const multer = require('multer');
const GridFsStorage = require('multer-gridfs-storage');
const Grid = require('gridfs-stream');
const methodOverride = require('method-override');

const mongoose = require('mongoose');
mongoose.connect("mongodb://localhost:27017/test1",{ useNewUrlParser: true , useUnifiedTopology: true });
var conn = mongoose.connection;

let gfs;
conn.once('open',function(){
  console.log("Connection Successful");
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection('uploads')
});

conn.on('error', console.error.bind(console, 'connection error:'));













var schema = new mongoose.Schema({  usermessage: [{text: String}],
                                                       sessionId: String});
var PersonModel = mongoose.model('Person', schema);

var newschema = new mongoose.Schema({ name : String, email: String, domain:String});
// var ContactModel = mongoose.model('Contact', newschema);
const contact = mongoose.Schema(
  {
      _id: mongoose.Schema.Types.ObjectId,
      Name: String,
      Email: String,
      Domain: String,
      Duration: String,
      
  }
);var Model = mongoose.model('contacts', contact);


const app = express();
const sessionId = uuid.v4();


app.use(function (req, res, next) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, OPTIONS, PUT, PATCH, DELETE"
  );
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-Requested-With,content-type"
  );
  res.setHeader("Access-Control-Allow-Credentials", true);

  // Pass to next layer of middleware
  next();
});

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);
app.use(methodOverride('_method'));
app.set("view engine", "ejs");
app.use(express.static("public", { maxAge: 2592000000 }));
var id= ""
// console.log(req.body.MSG);




// Create storage engine
const storage = new GridFsStorage({
  url: "mongodb://localhost:27017/test1",
  file: (req, file) => {
    return new Promise((resolve, reject) => {
      crypto.randomBytes(16, (err, buf) => {
        if (err) {
          return reject(err);
        }
        const filename = buf.toString('hex') + path.extname(file.originalname);
        const fileInfo = {
          filename: filename,
          bucketName: 'uploads'
        };
        resolve(fileInfo);
      });
    });
  }
});
const upload = multer({ storage });

// @route GET /
// @desc Loads form
app.get('/', (req, res) => {
  gfs.files.find().toArray((err, files) => {
    // Check if files
    if (!files || files.length === 0) {
      res.render('index', { files: false });
    } else {
      files.map(file => {
        if (
          file.contentType === 'image/jpeg' ||
          file.contentType === 'image/png'
        ) {
          file.isImage = true;
        } else {
          file.isImage = false;
        }
      });
      res.render('index', { files: files });
    }
  });
});

// @route POST /upload
// @desc  Uploads file to DB
app.post('/upload', upload.single('file'), (req, res) => {
  // res.json({ file: req.file });
  res.redirect('/');
});

// @route GET /files
// @desc  Display all files in JSON
app.get('/files', (req, res) => {
  gfs.files.find().toArray((err, files) => {
    // Check if files
    if (!files || files.length === 0) {
      return res.status(404).json({
        err: 'No files exist'
      });
    }

    // Files exist
    return res.json(files);
  });
});

// @route GET /files/:filename
// @desc  Display single file object
app.get('/files/:filename', (req, res) => {
  gfs.files.findOne({ filename: req.params.filename }, (err, file) => {
    // Check if file
    if (!file || file.length === 0) {
      return res.status(404).json({
        err: 'No file exists'
      });
    }
    // File exists
    return res.json(file);
  });
});

// @route GET /image/:filename
// @desc Display Image
app.get('/pdf/:filename', (req, res) => {
  gfs.files.findOne({ filename: req.params.filename }, (err, file) => {
    // Check if file
    if (!file || file.length === 0) {
      return res.status(404).json({
        err: 'No file exists'
      });
    }

    // Check if image
    if (file.contentType === 'application/pdf' || file.contentType === 'application/pdf') {
      // Read output to browser
      const readstream = gfs.createReadStream(file.filename);
      readstream.pipe(res);
    } 
    else {
      res.status(404).json({
        err: 'Not an pdf'
      });
    }
  });
});

// @route DELETE /files/:id
// @desc  Delete file
app.delete('/files/:id', (req, res) => {
  gfs.remove({ _id: req.params.id, root: 'uploads' }, (err, gridStore) => {
    if (err) {
      return res.status(404).json({ err: err });
    }

    res.redirect('/');
  });
});






app.post("/addcontact", (req, res) =>
  {
    console.log("Get body"+JSON.stringify(req.body))
    const  mybodydata = 
    {
        _id: new mongoose.Types.ObjectId(),
        Name:req.body.Name,
        Email: req.body.Email,
        Domain:req.body.Domain,
        Duration:req.body.Duration

    }
    var data2 = new  Model(mybodydata);
    data2.save( function(err)
    {
      if(err)
      {
          //console.log(data);
          res.send(data2,err);
      } else
      {
        console.log(data2)
          res.send(data2);
         
      }
    }) 
  })


app.post("/send-msg", (req, res) => {

  runSample(req.body.MSG).then((data) => {
     
    
      const p= new PersonModel({
        sessionId: sessionId,
        usermessage: [
         { text: req.body.MSG}
        ]
      });
       console.log(sessionId)
       //console.log(req.body.MSG)
       PersonModel.findByIdAndUpdate({_id: id }, {$push: {usermessage: {text: req.body.MSG}}}, {safe: true, upsert: true}, (err, r) => {
        if(!r)
        {
          p.save((p_err, p_res) => {
            if(p_err)
            console.log(p_err)
            else{
              id=p_res._id;
              console.log(p_res);
            }
            
          })
        }
        else{
          console.log(r)
        }
      })
    res.send({ Reply: data });
  });

    //if (res.send= 'Can you tell me your email please') {
      //var save= res.send({})
    //}

});

// app.get("/", function (req, res) {
//   res.render("index");
// });

/**
 * Send a query to the dialogflow agent, and return the query result.
 * @param {string} projectId The project to be used
 */
async function runSample(msg, projectId = "apiexample-xbgk") {
  // A unique identifier for the given session

  // Create a new session
  const sessionClient = new dialogflow.SessionsClient({
    keyFilename: "apiexample-xbgk-bc2f2d1daef0.json",
  });
  const sessionPath = sessionClient.projectAgentSessionPath(
    projectId,
    sessionId
  );

 

  // The text query request.
  const request = {
    session: sessionPath,
    queryInput: {
      text: {
        // The query to send to the dialogflow agent
        text: msg,
        // The language used by the client (en-US)
        languageCode: "en-US",
      },
    },
  };

  // Send request and log result
  const responses = await sessionClient.detectIntent(request);
  console.log("Detected intent");
  const result = responses[0].queryResult;
  console.log(`  Query: ${result.queryText}`);
  console.log(`  Response: ${result.fulfillmentText}`);
  if (result.intent) {
    console.log(`  Intent: ${result.intent.displayName}`);
  } else {
    console.log(`  No intent matched.`);
  }
  return result.fulfillmentText;
}

let port = process.env.PORT;
if (port == null || port == "") {
  port = 5000;
}

app.listen(port, () => {
  console.log("Running on port: " + port);
});