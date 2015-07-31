var
  http = require('http'),
  fs = require('fs'),
  qs = require('querystring'),
  exec = require('child_process').exec,
  url = require('url'),
  multiparty = require('multiparty');
  sqlite3 = require('sqlite3');
  path = require('path');
  PythonShell = require('python-shell');
var site = __dirname + '/public';
var urlobj;
var injectStatusAfter = '<!-- errors will go here -->';
var injectPasswordSectionAfter = 'onsubmit="saveFields()">';
var PythonOptions = {
  mode: 'text',
  scriptPath: '/usr/lib/edison_config_tools/public',
};
var mimeTypes = {'html': 'text/html', 
                 'png': 'image/png',
                 'js': 'text/javascript', 
                 'css': 'text/css'};
var db = new sqlite3.Database('/home/root/ProjectRidly/unified.db');	
var dbInsertStmt = db.prepare(' UPDATE calibrate SET AAunit=?, ABunit=?, BAunit=?, BBunit=? ,CAunit=?, CBunit=?,DAunit=?, DBunit=?, AAsel=?, AA_sen=?, AA_base=?, AA_zero=?, AA_span=?, ABsel=?, AB_sen=?, AB_base=?, AB_zero=?, AB_span=?, BAsel=?, BA_sen=?, BA_base=?, BA_zero=?, BA_span=?, BBsel=?, BB_sen=?, BB_base=?, BB_zero=?, BB_span=?, CAsel=?, CA_sen=?, CA_base=?, CA_zero=?, CA_span=?, CBsel=?, CB_sen=?, CB_base=?, CB_zero=?, CB_span=?, DAsel=?, DA_sen=?, DA_base=?, DA_zero=?,DA_span=?, DBsel=?, DB_sen=?, DB_base=?, DB_zero=?,DB_span=? WHERE id=1');
var dbSelectStmt = db.prepare('SELECT AAunit, ABunit, BAunit, BBunit, CAunit, CBunit, DAunit, DBunit, AAsel, AA_sen, AA_base, AA_zero, AA_span, ABsel, AB_sen, AB_base, AB_zero, AB_span, BAsel,  BA_sen, BA_base, BA_zero, BA_span, BBsel, BB_sen, BB_base, BB_zero, BB_span, CAsel, CA_sen, CA_base, CA_zero, CA_span, CBsel, CB_sen, CB_base, CB_zero, CB_span, DAsel, DA_sen, DA_base, DA_zero, DA_span, DBsel, DB_sen, DB_base, DB_zero, DB_span FROM calibrate ORDER BY id DESC');
//Edit db2SelectStmt limit to adjust amount of data shown on charts
var db2SelectStmt = db.prepare("SELECT address, time, temp, rh, pressure, address, type1, type2, adjusted1, adjusted2 FROM stack ORDER BY id DESC LIMIT 1000");
var supportedExtensions = {
  "css"   : "text/css",
  "xml"   : "text/xml",
  "htm"   : "text/html",
  "html"  : "text/html",
  "js"    : "application/javascript",
  "json"  : "application/json",
  "txt"   : "text/plain",
  "bmp"   : "image/bmp",
  "gif"   : "image/gif",
  "jpeg"  : "image/jpeg",
  "jpg"   : "image/jpeg",
  "png"   : "image/png"
};
var STATE_DIR = '/var/lib/edison_config_tools';
var NETWORKS_FILE = STATE_DIR + '/networks.txt';


function serveFromDisk(filename, res) {
    "use strict";
    var pathname;
    pathname = path.join(process.cwd(), filename);
    // SECURITY HOLE: Check for invalid characters in filename.
    // SECURITY HOLE: Check that this accesses file in CWD's hierarchy.
    path.exists(pathname, function (exists) {
        var extension, mimeType, fileStream;
        if (exists) {
            extension = path.extname(pathname).substr(1);
            mimeType = mimeTypes[extension] || 'application/octet-stream';
            res.writeHead(200, {'Content-Type': mimeType});
            console.log('serving ' + filename + ' as ' + mimeType);

            fileStream = fs.createReadStream(pathname);
            fileStream.pipe(res);
        } else {
            console.log('does not exist: ' + pathname);
            res.writeHead(404, {'Content-Type': 'text/plain'});
            res.write('404 Not Found\n');
            res.end();
        }
    }); //end path.exists
}
///
function fetchMessages(res) {
    "use strict";
    var jsonData;
    console.log('doing fetch');
    res.writeHead(200, {'Content-Type': 'application/json'});
    jsonData = { data: [] };
    dbSelectStmt.each(function (err, row) {
        jsonData.data.push({ AAunit: row.AAunit, ABunit: row.ABunit, BAunit: row.BAunit, BBunit: row.BBunit, CAunit: row.CAunit,  CBunit: row.CBunit, DAunit:  row.DAunit, DBunit: row.DBunit, AAsel: row.AAsel, AA_sen: row.AA_sen, AA_base: row.AA_base, AA_zero: row.AA_zero, AA_span: row.AA_span, ABsel: row.ABsel, AB_sen: row.AB_sen, AB_base: row.AB_base, AB_zero: row.AB_zero, AB_span: row.AB_span, BAsel: row.BAsel, BA_sen: row.BA_sen, BA_base: row.BA_base, BA_zero: row.BA_zero, BA_span: row.BA_span, BBsel: row.BBsel, BB_sen: row.BB_sen, BB_base: row.BB_base, BB_zero: row.BB_zero, BB_span: row.BB_span, CAsel: row.CAsel, CA_sen: row.CA_sen, CA_base: row.CA_base, CA_zero: row.CA_zero, CA_span: row.CA_span, CBsel: row.CBsel, CB_sen: row.CB_sen, CB_base: row.CB_base, CB_zero: row.CB_zero, CB_span: row.CB_span, DAsel: row.DAsel, DA_sen: row.DA_sen, DA_base: row.DA_base, DA_zero: row.DA_zero, DA_span: row.DA_span, DBsel: row.DBsel, DB_sen: row.DB_sen, DB_base: row.DB_base, DB_zero: row.DB_zero, DB_span: row.DB_span });
    }, function () {
        res.write(JSON.stringify(jsonData));
        res.end();
        //db.close
    });

}
///

///
function fetchData(res) {
    "use strict";

    var jsonData1;   
    console.log('doing fetch2');    
    jsonData1 = { data: [] };
    db2SelectStmt.each(function(err, row) {
    jsonData1.data.push({ address: row.address, time: row.time, temp: row.temp, rh: row.rh, pressure: row.pressure, type1: row.type1, value1: row.adjusted1, type2: row.type2, value2: row.adjusted2 });   
    }, function () {
        console.log(jsonData1);
	res.write(JSON.stringify(jsonData1));
        res.end(); 
        //db2.close       
   });

}

///
function processRequest(req, res) {
    "use strict";
    var uriobj;
    uriobj = url.parse(req.url).pathname;
   if (uriobj === '/fetch') {
        fetchMessages(res);
    } else if (uriobj === '/fetch2') {
        fetchData(res);
    } else if (uriobj === '/addnew') {
        addNewMessage(req, res);
    } else if (uriobj === '/start') {
        startService(req,res);
    } else if (uriobj === '/stop') {
        stopService(req,res);  
    } else if (uriobj === '/reset') {
        resetService(req,res);  
    } else if (uriobj === '/') {
        serveFromDisk('forum-base.html', res);
    } else {
        serveFromDisk(uriobj, res);
    }
}
///
function startService(req,res) {
    "use strict";
    console.log('doing start');

        // SECURITY HOLE: confirm name and message are reasonably short

	    serveFromDisk('/public/sensor.html', res);
        
        PythonShell.run('start_service.py', PythonOptions, function (err) {
          console.log('start');

    });

}
function resetService(req,res) {
    "use strict";
    console.log('doing reset');

        // SECURITY HOLE: confirm name and message are reasonably short

	    serveFromDisk('/public/sensor.html', res);
        
        PythonShell.run('reset_service.py', PythonOptions, function (err) {
          console.log('reset');

    });

}
///
function stopService(req,res) {
    "use strict";
    console.log('doing stop');

        // SECURITY HOLE: confirm name and message are reasonably short

	    serveFromDisk('/public/sensor.html', res);

        PythonShell.run('stop_service.py', PythonOptions, function (err) {
    
          console.log('Stop');

    });

}
///
///
function addNewMessage(req, res) {
    //var db = new sqlite3.Database('./public/ui.db');        
    //var dbInsertStmt = db.prepare('UPDATE calibrate SET AAunit=?, ABunit=?, BAunit=?, BBunit=? ,CAunit=?, CBunit=?,DAunit=?, DBunit=?,AAsel=?, AA_sen=?, AA_base=?, AA_zero=?, AA_span=?, ABsel=?, AB_sen=?, AB_base=?, AB_zero=?, AB_span=?, BAsel=?, BA_sen=?, BA_base=?, BA_zero=?, BA_span=?, BBsel=?, BB_sen=?, BB_base=?, BB_zero=?, BB_span=?, CAsel=?, CA_sen=?, CA_base=?, CA_zero=?, CA_span=?, CBsel=?, CB_sen=?, CB_base=?, CB_zero=?, CB_span=?, DAsel=?, DA_sen=?, DA_base=?, DA_zero=?,DA_span=?, DBsel=?, DB_sen=?, DB_base=?, DB_zero=?,DB_span=? WHERE id=1');
 
    "use strict";
    var postText = '';
    var uriobj;
    uriobj = url.parse(req.url).pathname;    
    console.log('doing add');
    req.setEncoding('utf8');
    req.addListener('data', function (postDataChunk) {
        postText += postDataChunk;
    });
    req.addListener('end', function () {
        // SECURITY HOLE: confirm name and message are reasonably short
        var postData = qs.parse(postText);
        dbInsertStmt.run( postData.AAunit, postData.ABunit, postData.BAunit, postData.BBunit, postData.CAunit, postData.CBunit, postData.DAunit, postData.DBunit, postData.AAsel, postData.AA_sen, postData.AA_base, postData.AA_zero, postData.AA_span, postData.ABsel, postData.AB_sen, postData.AB_base, postData.AB_zero, postData.AB_span,postData.BAsel, postData.BA_sen, postData.BA_base, postData.BA_zero, postData.BA_span,postData.BBsel, postData.BB_sen, postData.BB_base, postData.BB_zero, postData.BB_span, postData.CAsel, postData.CA_sen, postData.CA_base, postData.CA_zero, postData.CA_span, postData.CBsel, postData.CB_sen, postData.CB_base, postData.CB_zero, postData.CB_span, postData.DAsel, postData.DA_sen, postData.DA_base, postData.DA_zero, postData.DA_span, postData.DBsel, postData.DB_sen, postData.DB_base, postData.DB_zero, postData.DB_span, function () {
        
	    serveFromDisk('/public/sensor.html', res);
            updatedb();
        });
        //db_close();

    });
}
function updatedb() {
        PythonShell.run('db_update.py', PythonOptions, function (err) {
          console.log('update');
});
}

function getContentType(filename) {
  var i = filename.lastIndexOf('.');
  if (i < 0) {
    return 'application/octet-stream';
  }
  return supportedExtensions[filename.substr(i+1).toLowerCase()] || 'application/octet-stream';
}

function injectStatus(in_text, statusmsg, iserr) {
  var injectStatusAt = in_text.indexOf(injectStatusAfter) + injectStatusAfter.length;
  var status = "";
  if (statusmsg) {
    if (iserr)
      status = '<div id="statusarea" name="statusarea" class="status errmsg">' + statusmsg + '</div>';
    else
      status = '<div id="statusarea" name="statusarea" class="status">' + statusmsg + '</div>';
  }
  return in_text.substring(0, injectStatusAt) + status + in_text.substring(injectStatusAt, in_text.length);
}

function inject(my_text, after_string, in_text) {
  var at = in_text.indexOf(after_string) + after_string.length;
  return in_text.substring(0, at) + my_text + in_text.substring(at, in_text.length);
}

function pageNotFound(res) {
  res.statusCode = 404;
  res.end("The page at " + urlobj.pathname + " was not found.");
}

// --- end utility functions

function getStateBasedIndexPage() {
  if (!fs.existsSync(STATE_DIR + '/password-setup.done')) {
    return inject(fs.readFileSync(site + '/password-section.html', {encoding: 'utf8'}),
      injectPasswordSectionAfter,
      fs.readFileSync(site + '/index.html', {encoding: 'utf8'}));
  }
  return fs.readFileSync(site + '/index.html', {encoding: 'utf8'});
}

function setHost(params) {
  if (!params.name) {
    return {cmd: ""};
  }

  if (params.name.length < 5) {
    return {failure: "The name is too short. It must be at least 5 characters long."};
  }
  return {cmd: "configure_edison --changeName " + params.name};
}

function setPass(params) {
  if (fs.existsSync(STATE_DIR + '/password-setup.done')) {
    return {cmd: ""};
  }
  if (params.pass1 === params.pass2) {
    if (params.pass1.length < 8 || params.pass1.length > 63) {
      return {failure: "Passwords must be between 8 and 63 characters long. Please try again."};
    }
    return {cmd: "configure_edison --changePassword " + params.pass1};
  }
  return {failure: "Passwords do not match. Please try again."};
}

function setWiFi(params) {
  var exec_cmd = null, errmsg = "Unknown error occurred.";
  if (!params.ssid) {
    return {cmd: ""};
  } else if (!params.protocol) {
    errmsg = "Please specify the network protocol (Open, WEP, etc.)";
  } else if (params.protocol === "OPEN") {
    exec_cmd = "configure_edison --changeWiFi OPEN '" + params.ssid + "'";
  } else if (params.protocol === "WEP") {
    if (params.netpass.length == 5 || params.netpass.length == 13)
      exec_cmd = "configure_edison --changeWiFi WEP '" + params.ssid + "' '" + params.netpass + "'";
    else
      errmsg = "The supplied password must be 5 or 13 characters long.";
  } else if (params.protocol === "WPA-PSK") {
      if (params.netpass && params.netpass.length >= 8 && params.netpass.length <= 63) {
        exec_cmd = "configure_edison --changeWiFi WPA-PSK '" + params.ssid + "' '" + params.netpass + "'";
      } else {
        errmsg = "Password must be between 8 and 63 characters long.";
      }
  } else if (params.protocol === "WPA-EAP") {
      if (params.netuser && params.netpass)
        exec_cmd = "configure_edison --changeWiFi WPA-EAP '" + params.ssid + "' '" + params.netuser + "' '"
          + params.netpass + "'";
      else
        errmsg = "Please specify both the username and the password.";
  } else {
    errmsg = "The specified network protocol is not supported."
  }

  if (exec_cmd) {
    return {cmd: exec_cmd};
  }
  return {failure: errmsg};
}

function submitForm(params, res, req) {
  var calls = [setPass, setHost, setWiFi];
  var result = null, commands = ['sleep 5'];

  // check for errors and respond as soon as we find one
  for (var i = 0; i < calls.length; ++i) {
    result = calls[i](params, req);
    if (result.failure) {
      res.end(injectStatus(getStateBasedIndexPage(), result.failure, true));
      return;
    }
    commands.push(result.cmd);
  }

  // no errors occurred. Do success response.
  exec ('configure_edison --showNames', function (error, stdout, stderr) {
    var nameobj = {hostname: "unknown", ssid: "unknown"};
    try {
      nameobj = JSON.parse(stdout);
    } catch (ex) {
      console.log("Could not parse output of configure_edison --showNames (may not be valid JSON)");
      console.log(ex);
    }

    var hostname = nameobj.hostname;
    var res_str;
    var device_ap_ssid = nameobj.ssid;

    if (params.name) {
      hostname = params.name;
      device_ap_ssid = params.name;
    }

    if (params.ssid) { // WiFi is being configured
      res_str = fs.readFileSync(site + '/exit.html', {encoding: 'utf8'})
    } else {
      res_str = fs.readFileSync(site + '/exiting-without-wifi.html', {encoding: 'utf8'})
    }

    res_str = res_str.replace(/params_ssid/g, params.ssid); // leaves exiting-without-wifi.html unchanged
    res_str = res_str.replace(/params_hostname/g, hostname + ".local");
    res_str = res_str.replace(/params_ap/g, device_ap_ssid);
    res.end(res_str);

    // Now execute commands
    commands.push("configure_edison --disableOneTimeSetup");
    //commands.push("/home/root/vase.sh");
    for (var i = 0; i < commands.length; ++i) {
      if (!commands[i]) {
        continue;
      }
      console.log("Executing command: " + commands[i]);
      exec(commands[i], function(error, stdout, stderr) {
        if (error) {
          console.log("Error occurred:");
          console.log(stderr);
        }
        console.log(stdout);
      });
    }
  });
}

function handlePostRequest(req, res) {
     urlobj = url.parse(req.url, true);
    if (urlobj.pathname === '/addnew') {
        addNewMessage(req, res);
    } else if (urlobj.pathname === '/start') {
        startService(req, res);
    } else if (urlobj.pathname === '/stop') {
        stopService(req, res);
    } else if (urlobj.pathname === '/reset') {
        resetService(req, res);
    } else if (urlobj.pathname === '/submitForm') {
    var payload = "";
    req.on('data', function (data) {
      payload += data;
    });
    req.on('end', function () {
      var params = qs.parse(payload);
      submitForm(params, res, req);
    });
  } else if (urlobj.pathname === '/submitFirmwareImage') {
    var form = new multiparty.Form();

    form.parse(req, function(err, fields, files) {
      console.log(files);
      console.log('Upload completed!');

      if (err) {
        res.end(injectStatus(fs.readFileSync(site + '/upgrade.html', {encoding: 'utf8'}),
          "File upload failed. Please try again.", true));
      } else {
        var exitupgradeStr = fs.readFileSync(site + '/exit-upgrade.html', {encoding: 'utf8'});
        var currversion;
        exec('configure_edison --version ',
          function (error, stdout, stderr) {
            if (error) {
              currversion = "unknown";
            } else {
              currversion = stdout;
            }
            exitupgradeStr = exitupgradeStr.replace(/params_version/g, currversion);
            res.end(exitupgradeStr);

            exec('configure_edison --flashFile ' + files.imagefile[0].path,
              function (error, stdout, stderr) {
                if (error) {
                  console.log("Upgrade error: ");
                  console.log(stderr);
                  return;
                }
                console.log(stdout);
              });
          });
      }
    });
  } else {
    pageNotFound(res);
  }
}

// main request handler. GET requests are handled here.
// POST requests are handled in handlePostRequest()
function requestHandler(req, res) {

  urlobj = url.parse(req.url, true);

  // POST request. Get payload.
  if (req.method === 'POST') {
    handlePostRequest(req, res);
    return;
  }

  // GET request

  if (urlobj.pathname === '/fetch') {
        fetchMessages(res);
    } else if (urlobj.pathname === '/fetch2') {
        fetchData(res); 

    } else if (!urlobj.pathname || urlobj.pathname === '/' || urlobj.pathname === '/index.html') {
    if (fs.existsSync(STATE_DIR + '/one-time-setup.done')) {
      var res_str = fs.readFileSync(site + '/status.html', {encoding: 'utf8'});
      var myhostname, myipaddr;
      var cmd = 'configure_edison --showWiFiIP';
      console.log("Executing: " + cmd);
      exec(cmd, function (error, stdout, stderr) {
        if (error) {
          console.log("Error occurred:");
          console.log(stderr);
          myipaddr = "unknown";
        } else {
          myipaddr = stdout;
        }
        console.log(stdout);

        cmd = 'hostname';
        console.log("Executing: " + cmd);
        exec(cmd, function (error, stdout, stderr) {
          if (error) {
            console.log("Error occurred:");
            console.log(stderr);
            myhostname = "unknown";
          } else {
            myhostname = stdout;
          }
          console.log(stdout);

          res_str = res_str.replace(/params_ip/g, myipaddr);
          res_str = res_str.replace(/params_hostname/g, myipaddr);
          res.end(res_str);
        });
      });
//end first if
    } else {
      res.end(getStateBasedIndexPage());
    }
  } else if (urlobj.pathname === '/wifiNetworks') {
    if (fs.existsSync(NETWORKS_FILE)) {
      res.setHeader('content-type', getContentType(NETWORKS_FILE));
      res.end(fs.readFileSync(NETWORKS_FILE, {encoding: 'utf8'}));
    } else {
      res.statusCode = 404;
      res.end("Please try again later.");
    }
  } else { // for files like .css and images.
    if (!fs.existsSync(site + urlobj.pathname)) {
      pageNotFound(res);
      return;
    }
    fs.readFile(site + urlobj.pathname, function (err, data) {
      if (err)
        throw err;
      res.setHeader('content-type', getContentType(urlobj.pathname));
      res.end(data);
    });
  }
}///end requestHandler


http.createServer(requestHandler).listen(80);
