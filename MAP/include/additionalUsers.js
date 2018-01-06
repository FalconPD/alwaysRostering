"user strict";

var Papa = require("../include/papaparse");
var fs = require("fs");

var additionalUsers = [];

function addLine(teacher, school) {
  var line;
  var email;

  email = alwaysRostering.teacherEmail(teacher.id);

  line = {
    "School State Code": school.stateSchoolCode,
    "School Name": school.schoolName,
    "Instructor ID": teacher.id,
    "Instructor State ID": teacher.stateID,
    "Last Name": teacher.lastName,
    "First Name": teacher.firstName,
    "Middle Name": teacher.middleName,
    "User Name": email,
    "Email Address": email,
    "Role = School Proctor?": "Y",
    "Role = School Assessment Coordinator?": "",
    "Role = Administrator?": "",
    "Role = District Proctor?": "",
    "Role = Data Administrator?": "",
    "Role = District Assessment Coordinator?": "",
    "Role = Interventionist?": "",
    "Role = SN Administrator?": ""
  };
  additionalUsers.push(line);
};

function notIn(teacherID, schoolName) {
  var i;

  for (i = 0; i < additionalUsers.length; i++) {
    if ((additionalUsers[i]["School Name"] === schoolName) &&
        (additionalUsers[i]["Instructor ID"] === teacherID)) {
      return false;
    }
  }
  return true;
}

exports.create = function(roster) {
  var teacherID;
  var schoolName;
  var teacher;
  var school;

  additionalUsers = [];

  //Teachers may teach at multiple schools, so we need to make a list of unique
  //teacher school combinations from our roster
  roster.forEach(function(line) {
    teacherID = line["Instructor ID"];
    schoolName = line["School Name"];
    if (notIn(teacherID, schoolName)) {
      teacher = alwaysRostering.teacherInfo[teacherID];
      if (! teacher) {
        casper.echo("Warning: Unable to look up teacher " + teacherID);
        return;
      }
      school = alwaysRostering.getSchoolByName(schoolName);
      if (! school) {
        casper.echo("Warning: Unable to look up school " + schoolName);
        return;
      }
      addLine(teacher, school); 
    }
  });
};

exports.sort = function() {
  additionalUsers.sort(function(a, b) {
    var comparisons = ["School Name", "Last Name", "First Name"];
    var i;
    var key;
    var result;

    for (i = 0; i < comparisons.length; i++) {
      key = comparisons[i];
      
      result = a[key].localeCompare(b[key]);
      if (result !== 0) {
        return result;
      }
    }
    casper.echo("Warning: Duplicate lines in additionalUsers");
    casper.echo(JSON.stringify(a));
    casper.echo(JSON.stringify(b));
    return 0;
  });
};

exports.write = function(name) {
  var csv;

  csv = Papa.unparse(additionalUsers);
  fs.write(name, csv, "w");
};
