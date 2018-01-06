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
var roster = require("include/roster");
var additionalUsers = require("include/additionalUsers");
var diff = require("include/diff");
var timeStamp = new Date().getTime();
var rosterFile = "rosters/roster-" + timeStamp + ".csv";
var additionalUsersFile = "rosters/additionalUsers-" + timeStamp + ".csv";
var rosterUpdatesFile = "rosters/roster-updates-" + timeStamp + ".csv";
var additionalUsersUpdatesFile = "rosters/additionalUsers-updates-" +
  timeStamp + ".csv";

roster.create();
roster.check();
roster.sort();
roster.write(rosterFile);
additionalUsers.create(roster.getRoster());
additionalUsers.sort();
additionalUsers.write(additionalUsersFile);
diff.create("roster");
diff.write(rosterUpdatesFile);
diff.create("additionalUsers");
diff.write(additionalUsersUpdatesFile);

casper.exit();
