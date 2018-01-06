var require = patchRequire(require);
var fs = require("fs");
var rosterPrefix = "rosters/";

var lines = [];

function getLastTwo(filePrefix) {
  var path = "rosters/";
  var result = { last: "", secondToLast: "" };
  var re = new RegExp("^" + filePrefix + ".*\.csv");

  list = fs.list(path);
  list.forEach(function(filename) {
    if (filename.match(re)) {
      result.secondToLast = result.last;
      result.last = path + filename;
    }
  });
  return result;
}

function readArray(filename) {
  var data = fs.read(filename);
  return data.split(/\r*\n/);
};

function addNewLines(previous, current) {
  var oldRoster = readArray(previous);
  var newRoster = readArray(current);

  newRoster.forEach(function(line) {
    if (oldRoster.indexOf(line) === -1) {
      lines.push(line);
    }
  });
}

exports.create = function(filePrefix) {
  lines = [];
  var lastTwoFiles = getLastTwo(filePrefix);
  if ((lastTwoFiles.last === "") || (lastTwoFiles.secondToLast === "")) {
    casper.echo("Warning: Not enough roster files to make update file.");
    return;
  }
  addNewLines(lastTwoFiles.secondToLast, lastTwoFiles.last);
};

exports.write = function(filename) {
  if (lines.length === 0) {
    casper.echo("Warning: No new lines found, not writing file.");
    return;
  }
  fs.write(filename, lines.join("\n"));
};
