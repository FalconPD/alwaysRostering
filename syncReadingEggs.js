"use strict";

/**************************** Globals and Libraries ************************/
var casper = require("casper").create({
  verbose: true,
  logLevel: "debug",
  pageSettings: {
    loadImages: false,
    loadPlugins: false
  }
});
var utils = require("utils");
var alwaysRostering = require("./include/alwaysRostering");

/*************************** Steps in Sync Process *************************/
function login(username, password) {
  casper.then(function() {
    var url = "https://sso.readingeggs.com/login";

    this.echo("Logging in as " + username + "...");
    casper.open(url);
  });
  casper.then(function() {
    this.evaluate(function(username, password) {
      document.getElementById("username").value = username;
      document.getElementById("password").value = password;
      $("input[name='commit']").click();
    }, username, password);
  }).waitForUrl("https://app.readingeggs.com/re/teacher/dashboard");
}

function loadReadingEggsStudentInfo() {
  casper.then(function() {
    var url = "https://app.readingeggs.com/re/school/students.csv";
    var filename;

    filename = Date.now() + ".csv";
    this.echo("Loading student info from Reading Eggs...");
    casper.download(url, filename);
  });
}

/************************* Initialization **********************************/
alwaysRostering.init("syncReadingEggs.js");

/************************* Main Loop ***************************************/
var username;
var password;

username = alwaysRostering.credentials.readingEggs['MLS'].username;
password = alwaysRostering.credentials.readingEggs['MLS'].password;
login(username, password);
loadReadingEggsStudentInfo();

casper.run();
