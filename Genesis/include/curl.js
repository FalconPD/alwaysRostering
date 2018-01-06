"use strict";

var spawn = require("child_process").spawn;
var fs = require("fs");

var children = [];

function onExit(childData, httpCode) {
  //remove ourselves from the registry of running curl processes
  children.splice(childData.index, 1);

  //if our data is valid, move the temp file to the actual file
  if (httpCode === "200") {
    //move won't overwrite files, so delete if we have to
    if (fs.isFile(childData.file)) {
      fs.remove(childData.file);
    }
    fs.move(childData.tmpFile, childData.file);
  }
  else {
    console.log("curl: Unable to download file. Check '" + childData.tmpFile +
      "'."); 
  }
}
 
exports.download = function(url, filename) {
  //download to a temporary file
  var tmpFile = filename + ".temp";
  //use the cookies from phantom
  var cookiesArray = phantom.cookies.map(function(cookie) {
    return (cookie.name + "=" + cookie.value);
  });
  var curlCookies = cookiesArray.join(";");
  //write out the http code to stdout after the transfer is done
  var child = spawn("curl", [
    "--output", tmpFile,
    "--cookie", curlCookies,
    "--write-out", "%{http_code}",
    "--silent",
    "--compressed",
    url]);
  var childData = {
    child: child,
    file: filename,
    tmpFile: tmpFile,
    index: children.length
  }
  children.push(childData);
  child.stdout.on("data", function(httpCode) { onExit(childData, httpCode) }); 
};

exports.done = function() {
  return (children.length === 0);
};
