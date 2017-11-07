// This CasperJS module includes common functions used when
// syncing subscription websites with data from the SiS
var credentials = require("./credentials");
var Papa = require("./papaparse");
var require = patchRequire(require);
var fs = require("fs");

exports.dryRun = false;
exports.studentInfo = {};
exports.teacherInfo = {};
exports.credentials = credentials.credentials;
exports.studentReport;
exports.teacherReport;

exports.init = function(name) {
  casper.start();
  if (casper.cli.args.length !== 2) {
    casper.echo("Usage is " + name +
      " [--dry-run] <Student Report> <Teacher Report>");
    casper.exit();
  }
  exports.studentReport = casper.cli.args[0];
  exports.teacherReport = casper.cli.args[1];
  if (casper.cli.has("dry-run")) {
    exports.dryRun = true;
  }
};

//Returns hash with the key being Student ID for quick lookups
//takes the an array of grades, and an array of schools
exports.loadStudentReport = function(grades, schools) {
  console.log("Loading student report: " + exports.studentReport + " Grades: " +
              JSON.stringify(grades) + " Schools: " + JSON.stringify(schools));
  var content = fs.read(exports.studentReport);
  var parseResults = Papa.parse(content, {header: true});
  var data = parseResults.data;
  var hash = {};
  for (var i = 0; i < data.length; i++)
  {
    if ((schools.indexOf(data[i]['School Code']) != -1) &&
        (grades.indexOf(data[i]['Grade']) != -1)) {
      studentID = data[i]['Student ID'];
      delete data[i]['Student ID'];
      hash[studentID] = data[i]; 
    }
  }
  exports.studentInfo = hash;
}

exports.loadTeacherReport = function(schools) {
  var content;
  var parseResults;
  var data;
  var hash = {};
  var i;
  var teacherID;

  console.log("Loading teacher report: " + exports.teacherReport + " Schools: "
              + JSON.stringify(schools));
  content = fs.read(exports.teacherReport);
  parseResults = Papa.parse(content, {header: true});
  parseResults.data.forEach(function(line) {
    if (schools.indexOf(line.schoolCode) != -1) {
      teacherID = line.id;
      delete line.id;
      hash[teacherID] = line; 
    }
  });
  exports.teacherInfo = hash;
}

exports.jsonPost = function(url, data) {
  if (exports.dryRun) {
    console.log("Dry-run mode, skipping jsonPost");
  }
  else {
    casper.open(url, {method: 'post',
                      headers: {'Content-Type': 'application/json; charset=utf-8'},
                      encoding: 'utf8',
                      data: data});
  }
}

exports.post = function(url, data) {
  if (exports.dryRun) {
    console.log("Dummy mode, skipping post");
  }
  else {
    casper.open(url, {method: "post", data: data});
  }
}

//Prints a message about a student, looking up their first and last names
exports.studentMessage = function(studentID, prefix, msg) {
  console.log('[' + prefix + '] ' + studentID + ': ' +
              exports.studentInfo[studentID]['First Name'] + ' ' +
              exports.studentInfo[studentID]['Last Name'] + ' ' + msg);
}

exports.academicYear = function(studentID) {
  grade = exports.studentInfo[studentID]['Grade'];
  switch (grade) {
    case 'K':
      return 'Kindergarten';
    case '1':
      return '1st Grade';
    case '2':
      return '2nd Grade';
    case '3':
      return '3rd Grade';
    case '4':
      return '4th Grade';
    case '5':
      return '5th Grade';
    case '6':
      return '6th Grade';
    default:
      console.log('Unknown Grade: ' + grade);
      casper.exit();
  }
}

//Creates a student username in Eliot's format
exports.elementaryUsername = function(studentID) {
  var schoolCode = exports.studentInfo[studentID]['School Code'];
  switch (schoolCode) {
    case 'MLS':
      return 'ml' + studentID;
    case 'WES':
      return 'wl' + studentID;
    case 'BBS':
      return 'bb' + studentID;
    case 'BSE':
      return 'bs' + studentID;
    case 'OTS':
      return 'ot' + studentID;
    case 'AES':
      return 'ag' + studentID;
    default:
      console.log('Unknown School Code in elementaryUsername: ' + schoolCode);
      casper.exit();
  }
};

//Creates a student password in Eliot's format
exports.elementaryPassword = function(studentID) {
  var schoolCode = exports.studentInfo[studentID]['School Code'];
  switch (schoolCode) {
    case 'MLS':
      return 'ml123456';
    case 'WES':
      return 'wl123456';
    case 'BBS':
      return 'bb123456';
    case 'BSE':
      return 'bs123456';
    case 'OTS':
      return 'ot123456';
    case 'AES':
      return 'ag123456';
    default:
      console.log('Unknown School Code in elementaryPassword: ' + schoolCode);
      casper.exit();
  }
};

exports.gender = function(studentID) {
  genderCode = exports.studentInfo[studentID]['Gender Code'];
  switch (genderCode) {
    case 'M':
      return 'male';
    case 'F':
      return 'female';
    default:
      console.log('Unknown gender code in gender: ' + genderCode); 
      casper.exit();
  }
};

exports.teacherEmail = function(teacherID) {
  var teacher;
  var email;

  teacher = exports.teacherInfo[teacherID];
  email = teacher.firstName + "." + teacher.lastName + "@monroe.k12.nj.us";
  return email.replace(/[ \']/g, "");
}

//Creates and elementary teacher password in Eliot's format
exports.elementaryTeacherPassword = function(teacherID) {
  var schoolCode;

  schoolCode = exports.teacherInfo[teacherID].schoolCode;
  switch (schoolCode) {
    case "MLS":
      return "ml123456!";
    case "WES":
      return "wl123456!";
    case "BBS":
      return "bb123456!";
    case "BSE":
      return "bs123456!";
    case "OTS":
      return "ot123456!";
    case "AES":
      return "ag123456!";
    default:
      console.log("Unknown School Code in elementaryTeacherPassword: " +
                  schoolCode);
      casper.exit();
  }
};

exports.title = function(teacherID) {
  var teacher;

  teacher = exports.teacherInfo[teacherID];
  if (teacher.title !== "") {
    return teacher.title;
  }
  if (teacher.genderCode === "F") {
    return "Ms.";
  }
  else {
    return "Mr.";
  }
};
