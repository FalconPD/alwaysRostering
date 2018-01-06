"use strict";
var casper = require("casper").create({
  clientScripts: ["include/jquery-3.2.1.min.js"],
//  verbose: true,
//  logLevel: "debug",
  pageSettings: {
    loadImages: false,
    loadPlugins: false,
  }
});
var utils = require("utils");
var alwaysRostering = require("../include/alwaysRostering");
//Had to implement a curl library for large downloads
var curl = require("include/curl");

function login(username, password) {
  casper.then(function() {
    this.echo("Logging into Genesis as " + username + "...");
    this.open("https://genesis.monroe.k12.nj.us/genesis/sis/view");
  });
  casper.then(function() {
    this.evaluate(function(username, password) {
      $("#j_username").val(username);
      $("#j_password").val(password);
      $("#__submit1__").click();
    }, username, password);
  });
  casper.waitForSelector("img[title='Logout']");
}

function getReport(id, filename) {
  var minutes = 10; //the most time a report should take
  var timeout = minutes*60*1000;

  //make our post request  
  casper.then(function() {
    var data = {
      fldReportCode: id,
      rwFormat: "CSV",
      fldSchedulingOption: "NOW",
      fldRunAtDate: "",
      fldHour: "",
      fldMinute: "",
      fldAMPM: "",
      fldSchedYear: "*",
      fldSchedMonth: "*",
      fldSchedDay: "*",
      fldSchedHour: "*",
      fldSchedMinute: "*",
      paramSSORT_SET_CODE: "DEF",
      paramSMAKESTUDENTLIST: "",
      fldEmailUser: ""
    };
    var url = "https://genesis.monroe.k12.nj.us/genesis/sis/view?" +
      "module=reportWriter&" +
      "category=reports&" + 
      "tab1=scheduleReport&" +
      "action=performQueueReport";
    
    this.echo("Generating report " + id + ". This could take up to " +
      minutes + " minutes...");
    alwaysRostering.post(url, data);
  });

  casper.then(function() {
    this.waitFor(function check() {
      //wait for the download button to show up
      return this.evaluate(function() {
        return ($("button[value='Download Output']").length > 0);
      });
    },
    function then() {
      //pull the runcode out of window.location
      var re=/runcode=(.*?)(&|$)/;
      var result = re.exec(this.getGlobal("location").href);
      var runcode = result[1];

      //create our download URL and download
      var url = "https://genesis.monroe.k12.nj.us/genesis/sis/view?" +
        "module=reportWriter&" +
        "category=reports&" +
        "tab1=viewReport&" +
        "runcode=" + runcode + "&" +
        "action=rawopen";
      this.echo("Downloading report to '" + filename + "' in background...");
//      this.download(url, filename);
      curl.download(url, filename);
    },
    function timedout() {
      this.echo("Timed out waiting for report to finish.");
      this.exit();
    },
    timeout);
  });
}

function waitForDownloads() {
  var minutes = 5;
  var timeout = minutes*60*1000;

  casper.then(function() {
    this.echo("Waiting for downloads to finish. This could take up to " +
      minutes + " minutes.");
    this.waitFor(curl.done,
      function then() {
        this.echo("All downloads complete.");
      },
      function timedout() {
        this.echo("Timed out waiting for downloads.");
      },
      timeout);
  });
}

var username = alwaysRostering.credentials.genesis.username;
var password = alwaysRostering.credentials.genesis.password;
//from largest to smallest to take advantage of background downloading
var reports = [
  {id: "991007", filename: "reports/classes.csv" },
  {id: "990990", filename: "reports/students.csv" },
  {id: "990989", filename: "reports/teachers.csv" },
  {id: "991009", filename: "reports/schools.csv" }
];

login(username, password);
reports.forEach(function(report) {
  getReport(report.id, report.filename);
});
waitForDownloads();

casper.run();
