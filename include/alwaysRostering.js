// This CasperJS module includes common functions used when
// syncing subscription websites with data from the SiS
var credentials = require("./credentials");
var Papa = require("./papaparse");
var require = patchRequire(require);
var fs = require("fs");

exports.studentInfo = {};
exports.teacherInfo = {};
exports.classInfo = [];
exports.schoolInfo = {};
exports.credentials = credentials.credentials;
exports.studentReport = "../reports/students.csv";
exports.teacherReport = "../reports/teachers.csv";
exports.classReport = "../reports/classes.csv";
exports.schoolReport = "../reports/schools.csv";

casper.start();

exports.dryRun = false;
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

exports.loadSchoolReport = function() {
  var content;
  var parseResults;

  console.log("Loading school report");
  exports.schoolInfo = {};
  content = fs.read(exports.schoolReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  parseResults.data.forEach(function(line) {
    exports.schoolInfo[line.schoolCode] = line;
  });
};
  
exports.loadClassReport = function(schools) {
  var content;
  var parseResults;

  console.log("Loading class report: " + exports.classReport + " Schools: " +
    JSON.stringify(schools));
  exports.classInfo = [];
  content = fs.read(exports.classReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  parseResults.data.forEach(function(line) {
    if (schools.indexOf(line.schoolCode) != -1) {
      exports.classInfo.push(line);
    }
  });
};

exports.studentsInClass = function(school, course, section) {
  var studentIDs = [];

  exports.classInfo.forEach(function(entry) {
    if ((entry.schoolCode === school) &&
        (entry.courseCode === course) &&
        (entry.courseSection === section)) {
      studentIDs.push(entry.studentID);
    }
  });
  return studentIDs;
};

//Returns hash with the key being Student ID for quick lookups
//takes the an array of grades, and an array of schools
exports.loadStudentReport = function(schools, grades) {
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
      exports.studentInfo[studentID] = line;
    }
  });
};

//Internal function that takes care of some issues we have with the teacher
//report data
function cleanTeacherLine(line) {
  var gradeLevel;
  var last;

  //We have to remove leading zeros from gradeLevel
  gradeLevel = line.gradeLevel.replace(/^0+/, "");
  line.gradeLevel = gradeLevel;

  //Trim the AM/PM from the end of kindergarten/preschool teacher's names
  //but make sure we store the info
  line.half = "";
  if ((line.gradeLevel === "KH") ||
      (line.gradeLevel === "KF") ||
      (line.gradeLevel === "4H") ||
      (line.gradeLevel === "4F")) {
    if (/\s+PM$/.test(line.lastName)) {
      line.half = "PM";
    }
    else if (/\s+AM$/.test(line.lastName)) {
      line.half = "AM";
    }
    last = line.lastName.replace(/\s+PM$|\s+AM$/, "");
    line.lastName = last;
  }

  return line;
}

//this loads a teacher report and OVERWRITES any previous data
exports.loadTeacherReport = function(schools, grades) {
  var content;
  var parseResults;
  var data;
  var hash = {};
  var i;
  var teacherID;
  var gradeLevel;
  var last;

  casper.echo("Loading teacher report: " + exports.teacherReport + " Schools: "
              + JSON.stringify(schools) + " Grades: " +
              JSON.stringify(grades));
  content = fs.read(exports.teacherReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  parseResults.data.forEach(function(origLine) {
    line = cleanTeacherLine(origLine);
    if (schools.length > 0) {
      if (schools.indexOf(line.schoolCode) === -1) {
        return;
      }
    }
    if (grades.length > 0) {
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
//note that teachers may be repeated in the report if they are in multiple
//building, so a schoolCode should be specified
exports.addTeacher = function(schoolCode, teacherID) {
  var content;
  var parseResults;
  var notFound = true;
  var gradeLevel;
  var last;

  content = fs.read(exports.teacherReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  parseResults.data.forEach(function(origLine) {
    line = cleanTeacherLine(origLine);
    if (schoolCode !== line.schoolCode) {
        return;
    }
    if (teacherID === line.id) {
      exports.teacherInfo[teacherID] = line;
      casper.echo("Adding teacher " + line.firstName + " " + line.lastName + " "
        + schoolCode + " to teacherInfo.");
      notFound = false;
    }
  });
  if (notFound) {
    capser.echo("addTeacher: Unable to load info for teacherID " + teacherID +
      " " + schoolCode);
    casper.exit();
  }
};

//Adds a group of students to studentInfo
//takes an array of studentIDs
exports.addStudents = function(studentIDs) {
  var content;
  var parseResults;

  content = fs.read(exports.studentReport);
  parseResults = Papa.parse(content, {header: true, skipEmptyLines: true});
  studentIDs.forEach(function(studentID) {
    parseResults.data.forEach(function(line) {
      if (line.id === studentID) {
        exports.studentInfo[studentID] = line;
        casper.echo("Adding student " + line.id + " " + line.firstName + " " +
          line.lastName + " to studentInfo.");
      }
    });
  });
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
    case "BES":
      return "bs" + studentID;
    case "OTS":
      return "ot" + studentID;
    case "AES":
      return "ag" + studentID;
    case "AMS":
      return "ms" + studentID;
    case "MTHS":
      return "hs" + studentID;
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
    case "BES":
      return "bs123456";
    case "OTS":
      return "ot123456";
    case "AES":
      return "ag123456";
    case "AMS":
      return "ms123456";
    case "MTHS":
      return "hs123456";
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

exports.studentEmail = function(studentID) {
  var student;
  var email;
  
  student = exports.studentInfo[studentID];
  if (student.networkID === "") {
    return "";
  }
  else {
    email = student.networkID + "@students.monroe.k12.nj.us";
    return email;
  }
};

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
exports.hrTeacherFirstLast = function(studentID) {
  var teacherID;
  var teacher;
  var grade;
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
  return teacher.firstName + " " + teacher.lastName;
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
  var first;
  var last; 

  for (teacherID in exports.teacherInfo) {
    teacher = exports.teacherInfo[teacherID];
    if ((teacher.firstName === firstName) && (teacher.lastName === lastName)
        && (teacher.sharedTeacher === "N")) {
      return teacherID;
    }
  }
  return false;
};

exports.getSchoolByName = function(name) {
  var school;

  for (schoolCode in exports.schoolInfo) {
    school = exports.schoolInfo[schoolCode];
    if (school.schoolName === name) {
      return school;
    }
  }
  return false;
};
