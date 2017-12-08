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
  casper.on('remote.message', function(message) {
    this.echo("remote.message: " + message);
  });
  casper.on("page.error", function(msg, trace) {
    this.echo("page.error: " + msg);
    this.exit();
  });
};

//FIXME: Swap schools and grades order in arguments to be consistent with
//loadTeacherReport
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
    if ((schools.indexOf(data[i].schoolCode) != -1) &&
        (grades.indexOf(data[i].grade) != -1)) {
      studentID = data[i].id;
      delete data[i].id;
      hash[studentID] = data[i]; 
    }
  }
  exports.studentInfo = hash;
};

//This adds the students of a particular HR teacher at a particular school
//to studentInfo. Make sure you've loaded the teacher's info before you run this
exports.addHRTeacherStudents = function(school, teacherID) {
  var content;
  var teacher;
  var parseResults;
  var studentID;

  teacher = exports.teacherInfo[teacherID];
  if (! (teacher)) {
    casper.echo("addHRTeacherStudents: Unable to look up teacherID " +
                teacherID + " in file " + exports.teacherReport);
    casper.exit();
  }
  console.log("Adding " + school + " " + teacher.firstName + " " +
              teacher.lastName + "'s students to studentInfo");
  content = fs.read(exports.studentReport);
  parseResults = Papa.parse(content, {header: true});
  parseResults.data.forEach(function(line) {
    if ((line.schoolCode === school) && (line.hrTeacherID === teacherID)) {
      studentID = line.id;
      delete line.id;
      exports.studentInfo[studentID] = line;
    }
  });
};

//this loads a teacher report and OVERWRITES any previous data
exports.loadTeacherReport = function(schools, grades) {
  var content;
  var parseResults;
  var data;
  var hash = {};
  var i;
  var teacherID;
  var gradeLevel;

  casper.echo("Loading teacher report: " + exports.teacherReport + " Schools: "
              + JSON.stringify(schools) + " Grades: " +
              JSON.stringify(grades));
  content = fs.read(exports.teacherReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  parseResults.data.forEach(function(line) {
    //We have to remove leading zeros from gradeLevel in the teacher report
    gradeLevel = line.gradeLevel.replace(/^0+/, "");
    line.gradeLevel = gradeLevel;
    if (schools) {
      if (schools.indexOf(line.schoolCode) === -1) {
        return;
      }
    }
    if (grades) {
      if (grades.indexOf(line.gradeLevel) === -1) {
        return;
      }
    }
    teacherID = line.id;
    hash[teacherID] = line; 
  });
  exports.teacherInfo = hash;
};

//Adds a teacher to teacherInfo. This is useful if you have extra teachers
//from other buildings/grades who may need their students rostered
exports.addTeacher = function(teacherID) {
  var content;
  var parseResults;
  var notFound = true;

  content = fs.read(exports.teacherReport);
  parseResults = Papa.parse(content, {header: true});
  parseResults.data.forEach(function(line) {
    if (teacherID === line.id) {
      delete line.id;
      exports.teacherInfo[teacherID] = line;
      console.log("Adding " + line.firstName + " " + line.lastName +
                  " to teacherInfo");
      notFound = false;
    }
  });
  if (notFound) {
    casper.echo("addTeacher: Unable to load info for teacherID " + teacherID);
    casper.exit();
  }
};

exports.jsonPost = function(url, data) {
  if (exports.dryRun) {
    console.log("Dry-run mode, skipping jsonPost");
  }
  else {
    casper.open(url, {
      method: 'post',
      headers: {'Content-Type': 'application/json; charset=utf-8'},
      encoding: 'utf8',
      data: data
    });
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
              exports.studentInfo[studentID].firstName + ' ' +
              exports.studentInfo[studentID].lastName + ' ' + msg);
}

//Currently used by EducationCity
exports.academicYear = function(studentID) {
  var grade;

  grade = exports.studentInfo[studentID].grade;
  switch (grade) {
    case "KH":
    case "KF":
      return "Kindergarten";
    case "1":
      return "1st Grade";
    case "2":
      return "2nd Grade";
    case "3":
      return "3rd Grade";
    case "4":
      return "4th Grade";
    case "5":
      return "5th Grade";
    case "6":
      return "6th Grade";
    default:
      console.log("Unknown Grade: " + grade);
      casper.exit();
  }
}

//gets rid of some of the non-standard grades listed in Genesis
exports.basicGrade = function(studentID) {
  var grade;

  grade = exports.studentInfo[studentID].grade;
  switch (grade) {
    case "KH":
    case "KF":
      return "K";
    default:
      return grade;
  }
};

//Creates a student username in Eliot's format
exports.elementaryUsername = function(studentID) {
  var schoolCode;

  schoolCode = exports.studentInfo[studentID].schoolCode;
  switch (schoolCode) {
    case "MLS":
      return "ml" + studentID;
    case "WES":
      return "wl" + studentID;
    case "BBS":
      return "bb" + studentID;
    case "BSE":
      return "bs" + studentID;
    case "OTS":
      return "ot" + studentID;
    case "AES":
      return "ag" + studentID;
    case "AMS":
      return "ms" + studentID;
    default:
      casper.echo("elementaryUsername: Unknown School Code: " + schoolCode);
      casper.exit();
  }
};

//Creates a student password in Eliot's format
exports.elementaryPassword = function(studentID) {
  var schoolCode;

  schoolCode = exports.studentInfo[studentID].schoolCode;
  switch (schoolCode) {
    case "MLS":
      return "ml123456";
    case 'WES':
      return "wl123456";
    case "BBS":
      return "bb123456";
    case "BSE":
      return "bs123456";
    case "OTS":
      return "ot123456";
    case "AES":
      return "ag123456";
    case "AMS":
      return "ms123456";
    default:
      casper.echo("elementaryPassword: Unknown school code: " + schoolCode);
      casper.exit();
  }
};

exports.gender = function(studentID) {
  var genderCode;

  genderCode = exports.studentInfo[studentID].genderCode;
  switch (genderCode) {
    case "M":
      return "male";
    case "F":
      return "female";
    default:
      casper.echo("gender: Unknown gender code: " + genderCode); 
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

//Determines if a student record needs to be updated
//Takes an array of arrays with three elements and a studentID
//comparisons[0] is the title of the comparison and comparisons[1 and 2] are
//the two things to compare. Returns true if the record needs updating
exports.needsUpdate = function(comparisons, studentID) {
  for (i = 0; i < comparisons.length; i++) {
    if (comparisons[i][1] != comparisons[i][2]) {
      exports.studentMessage(studentID, "UPDATE", comparisons[i][0] +
        " does not match (" + comparisons[i][1] + "->" + comparisons[i][2] +
        ")");
      return true;
    }
  }
};

//returns "FirstName LastName" for a homeroom teacher
//will return the FIRST real teacher if the homeroom teacher is a shared teacher
//will chop the PM/AM off the end of a kindergarten teachers name
exports.hrTeacherFirstLast = function(studentID) {
  var teacherID;
  var teacher;
  var grade;
  var firstName;
  var lastName;
  var newID;

  teacherID = exports.studentInfo[studentID].hrTeacherID;
  grade = exports.studentInfo[studentID].grade;
  if (! (teacherID in exports.teacherInfo)) {
    casper.echo("hrTeacherFirstLast: Unable to find teacherID (" + teacherID +
                ") in teacherInfo.");
    casper.exit();
  }
  teacher = exports.teacherInfo[teacherID];
  if (teacher.sharedTeacher === "Y") {
    newID = teacher.sharedTeacherID1;
    if (! (newID in exports.teacherInfo)) {
      casper.echo("hrTeacherFirstLast: Unable to find sharedTeacherID1 (" + newID + ") in teacherInfo.");
      casper.exit();
    }
    teacher = exports.teacherInfo[newID];
  }
  firstName = teacher.firstName;
  switch (grade) {
    case "KH":
    case "KF":
      lastName = teacher.lastName.replace(/ PM$| AM$/, ""); 
    break;
    default:
      lastName = teacher.lastName;
  }
  return firstName + " " + lastName;
};

//See if we can find a student by first and last name. Ignores beginning
//and ending whitespace as well as capitalization
exports.lookupStudent = function(firstName, lastName) {
  var studentID;

  for (studentID in exports.studentInfo) {
    if ((exports.studentInfo[studentID].firstName.toUpperCase() ===
         firstName.trim().toUpperCase()) &&
        (exports.studentInfo[studentID].lastName.toUpperCase() ===
         lastName.trim().toUpperCase())) {
      return studentID;
    }
  }
  return false;
};

//returns the first non-shared teacher that matches first and last name.
exports.lookupTeacher = function(firstName, lastName) {
  var teacherID;
  var teacher;

  for (teacherID in exports.teacherInfo) {
    teacher = exports.teacherInfo[teacherID]; 
    if ((teacher.firstName === firstName) && (teacher.lastName === lastName)
        && (teacher.sharedTeacher === "N")) {
      return teacherID;
    }
  }
  return false;
};
