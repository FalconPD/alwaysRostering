"use strict";

var casper = require("casper").create({
//  verbose: true,
//  logLevel: "debug",
  pageSettings: {
    loadImages: false,
    loadPlugins: false
  }
});
var alwaysRostering = require("../include/alwaysRostering");
var roster = require("./roster");
var additionalUsers = require("./additionalUsers");
var timeStamp = new Date().getTime();
var rosterFile = "rosters/roster-" + timeStamp + ".csv";
var additionalUsersFile = "rosters/additionalUsers-" + timeStamp + ".csv";

roster.create();
roster.check();
roster.sort();
roster.write(rosterFile);
additionalUsers.create(roster.getRoster());
additionalUsers.sort();
additionalUsers.write(additionalUsersFile);

casper.exit();
