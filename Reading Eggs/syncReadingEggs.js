"use strict";

/**************************** Globals and Libraries ************************/
var casper = require("casper").create({
//  verbose: true,
//  logLevel: "debug",
  pageSettings: {
    loadImages: false,
    loadPlugins: false
  },
  clientScripts: [
    "../include/limit.js",
    "requests.js"
  ]
});
var utils = require("utils");
var alwaysRostering = require("../include/alwaysRostering");
var readingEggsStudentInfo = [];
var readingEggsTeacherInfo = [];

/*************************** Utility Functions *****************************/
function lookupReadingEggsStudent(studentId) {
  var i;
  var student;

  for (i = 0; i < readingEggsStudentInfo.length; i++) {
    student = readingEggsStudentInfo[i];
    if (student.studentId === studentId) {
      return student;
    }
  }
  return false;
}

//Teachers don't have an external ID in Reading Eggs, so we have to look them
//up by first and last name
function lookupReadingEggsTeacher(teacherID) {
  var i;
  var rTeacher;
  var gTeacher;

  gTeacher = alwaysRostering.teacherInfo[teacherID];
  for (i = 0; i < readingEggsTeacherInfo.length; i++) {
    rTeacher = readingEggsTeacherInfo[i];
    if ((rTeacher.firstName === gTeacher.firstName) &&
        (rTeacher.lastName === gTeacher.lastName)) {
      return rTeacher;
    }
  }
  return false;
}

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

function setupTeacherPage() {
  casper.then(function() {
    this.echo("Loading teacher info from Reading Eggs...");
    this.open("https://app.readingeggs.com/re/school/teachers");
  });
  casper.then(function() {
    casper.page.injectJs("teachers.js");
  });
}

function waitForRequests(type) {
  var test;

  switch(type) {
    case "teacher":
      test = function() { return teacherRequests.done(); };
      break;
    case "student":
      test = function() { return studentRequests.done(); };
      break;
    default:
      casper.echo("waitForRequests: Unknown request type " + type);
      casper.exit();
  }
  casper.then(function() {
    casper.waitFor(
      function() { return casper.evaluate(test); },
      function then() {},
      function onTimeout() {
        casper.echo("Timed out waiting for requests.");
      },
      60*5*1000 //take up to five minutes
    );
  });
}

function loadReadingEggsTeacherInfo() {
  casper.thenEvaluate(function() { teacherRequests.load(); });
}

function getReadingEggsTeacherInfo() {
  casper.then(function() {
    readingEggsTeacherInfo = casper.evaluate(function() {
      return teacherRequests.get();
    });
  });
}

function ignoreAdminAccount(adminLogin) {
  casper.then(function() {
    var i;

    for (i = 0; i < readingEggsTeacherInfo.length; i++) {
      if (readingEggsTeacherInfo[i].login === adminLogin) {
        readingEggsTeacherInfo.splice(i, 1);
      }
    }
  });
}

function updateDeleteTeachers() {
  casper.then(function() {
    var deletes = [];

    readingEggsTeacherInfo.forEach(function(rTeacher) {
      var teacherID;
      var gTeacher;
      var gTeacherEmail;
      var needsUpdate = false;
      var editData;

      //We don't have IDs for teachers in ReadingEggs so we have to look
      //them up by their first and last name
      teacherID = alwaysRostering.lookupTeacher(rTeacher.firstName,
        rTeacher.lastName);
      if (teacherID) {
        gTeacher = alwaysRostering.teacherInfo[teacherID];
        gTeacherEmail = alwaysRostering.teacherEmail(teacherID);
        //The only things we may update are their login and email
        if (rTeacher.email !== gTeacherEmail) {
          casper.echo("[UPDATE] " + teacherID + ": " + gTeacher.firstName +
            " " + gTeacher.lastName + " Email: " + rTeacher.email + "->" +
            gTeacherEmail);
          needsUpdate = true;
        }
        if (rTeacher.login !== gTeacherEmail) {
          casper.echo("[UPDATE] " + teacherID + ": " + gTeacher.firstName +
            " " + gTeacher.lastName + " Login: " + rTeacher.login + "->" +
            gTeacherEmail);
          needsUpdate = true;
        }
        if (needsUpdate) {
          if (alwaysRostering.dryRun) {
            casper.echo("Dry run option set, not updating.");
          } else {
            //NOTE: We don't update the password
            editData = {
              login: gTeacherEmail,
              firstName: gTeacher.firstName,
              lastName: gTeacher.lastName,
              email: gTeacherEmail,
              password: "",
              readingEggsID: rTeacher.id
            };  
            
            casper.evaluate(function(editData) {
              teacherRequests.edit(editData);
            }, editData);
          }
        }
      } else {
        casper.echo("[DELETE] " + rTeacher.firstName + " " + rTeacher.lastName);
        deletes.push(rTeacher.id);
      }
    });
    if (deletes.length !== 0) {
      if (alwaysRostering.dryRun) {
        casper.echo("Dry run option set, not deleting.");
      } else {
        casper.evaluate(function(ids) { teacherRequests.del(ids); }, deletes);
      }
    }
  });
}

function addTeachers() {
  casper.then(function() {
    for (teacherID in alwaysRostering.teacherInfo) {
      var teacher = {};
      var teacherID;
      var addInfo;

      teacher = alwaysRostering.teacherInfo[teacherID];

      //Don't add Kindergarten teachers with PM or AM after their name
      if ((teacher.gradeLevel === "KH") || (teacher.gradeLevel === "KF")) {
        if (/ PM$| AM$/.test(teacher.lastName)) {
          continue;
        }
      }

      //Don't add shared teachers
      if (teacher.sharedTeacher === "Y")
        continue;

      if (! lookupReadingEggsTeacher(teacherID)) {
        casper.echo("[ADD] " + teacherID + ": " + teacher.firstName + " " +
          teacher.lastName + " " + teacher.schoolCode + " " +
          teacher.gradeLevel);
        if (alwaysRostering.dryRun) {
          casper.echo("Dry run option set, not adding.");
        } else {
          addInfo = {
            firstName: teacher.firstName,
            lastName: teacher.lastName,
            email: alwaysRostering.teacherEmail(teacherID)
          };
          casper.evaluate(function(addInfo) {
            teacherRequests.add(addInfo);
          }, addInfo);
        }
      }
    }
  });
}
 
function setupStudentPage() {
  casper.then(function() {
    this.echo("Loading student info from Reading Eggs...");
    this.open("https://app.readingeggs.com/re/school/students");
  });
  casper.then(function() {
    casper.page.injectJs("students.js");
  });
}

function loadReadingEggsStudentInfo() {
  casper.thenEvaluate(function() { studentRequests.load(); });
}

function getReadingEggsStudentInfo() {
  casper.then(function() {
    readingEggsStudentInfo = casper.evaluate(function() {
      return studentRequests.get();
    });
  });
}

function updateDeleteStudents() {
  casper.then(function() {
    var deletes = [];

    readingEggsStudentInfo.forEach(function(rstudent) {
      var studentID;
      var gstudent;
      var comparisons = [];
      var needsUpdate = false;
      var editInfo;
    
      studentID = rstudent.studentId;
      if (studentID === "") {
        studentID = alwaysRostering.lookupStudent(rstudent.firstName,
          rstudent.lastName);
        if (studentID) {
          alwaysRostering.studentMessage(studentID, "UPDATE",
                                         "needs studentId added");
          gstudent = alwaysRostering.studentInfo[studentID];
          needsUpdate = true;
        } else {
          casper.echo("[DELETE] " + rstudent.firstName + " " +
                      rstudent.lastName +
                      " does not have studentId, could not look up");
          deletes.push(rstudent.id);
        }
      } else if (studentID in alwaysRostering.studentInfo) {
        gstudent = alwaysRostering.studentInfo[studentID];
        comparisons = [
          ["First Name", rstudent.firstName, gstudent.firstName],
          ["Last Name", rstudent.lastName, gstudent.lastName],
          ["Grade", rstudent.gradeName, alwaysRostering.basicGrade(studentID)],
          ["Login", rstudent.login,
            alwaysRostering.elementaryUsername(studentID)],
          ["Class Name", rstudent.teacherNames,
            alwaysRostering.hrTeacherFirstLast(studentID)]
        ];
        if (alwaysRostering.needsUpdate(comparisons, studentID)) {
          needsUpdate = true;
        }
      } else {
        casper.echo("[DELETE] " + rstudent.studentId + ": " + rstudent.firstName
                    + " " + rstudent.lastName);
        deletes.push(rstudent.id);
      }
      if (needsUpdate) {
        if (alwaysRostering.dryRun) {
          casper.echo("Dry run option set, not updating.");
        } else {
          editInfo = {
            firstName: gstudent.firstName,
            lastName: gstudent.lastName,
            grade: alwaysRostering.basicGrade(studentID),
            className: alwaysRostering.hrTeacherFirstLast(studentID),
            login: alwaysRostering.elementaryUsername(studentID),
            password: alwaysRostering.elementaryPassword(studentID),
            studentID: studentID,
            readingEggsID: rstudent.id
          };
          casper.evaluate(function(editInfo) {
            studentRequests.edit(editInfo);
          }, editInfo);
        }
      }
    });
    if (alwaysRostering.dryRun) {
      casper.echo("Dry run option set, not deleting.");
    } else {
      //TODO: Implement student deletes
    }
  });
}

function addStudents() {
  casper.then(function() {
    var student = {};
    var studentID;

    for (studentID in alwaysRostering.studentInfo) {
      student = alwaysRostering.studentInfo[studentID];
      if (! lookupReadingEggsStudent(studentID)) {
        alwaysRostering.studentMessage(studentID, "ADD", ""); 
        if (alwaysRostering.dryRun) {
          casper.echo("Dry run option set, not adding.");
        } else {
          //TODO: Implement student adds
        }
      }
    }
  });
}

/************************* Initialization **********************************/
alwaysRostering.init("syncReadingEggs.js");

/************************* Main Loop ***************************************/
var username;
var password;

//Mill Lake - All K-2 students and teachers
alwaysRostering.loadStudentReport(["KF", "KH", "1", "2"], ["MLS"]);
alwaysRostering.loadTeacherReport(["MLS"], ["KF", "KH", "1", "2"]);
//Also the Woodland self-contained class
alwaysRostering.addTeacher("8016");
alwaysRostering.addHRTeacherStudents("WES", "8016");
//And self-contained teachers at Mill Lake (no Grade Level in Genesis)
alwaysRostering.addTeacher("6649");
alwaysRostering.addTeacher("432");
alwaysRostering.addTeacher("8020");

username = alwaysRostering.credentials.readingEggs["MLS"].username;
password = alwaysRostering.credentials.readingEggs["MLS"].password;

login(username, password);
setupTeacherPage();
loadReadingEggsTeacherInfo();
waitForRequests("teacher");
getReadingEggsTeacherInfo();
ignoreAdminAccount(username);
updateDeleteTeachers();
addTeachers();
waitForRequests("teacher");
setupStudentPage();
loadReadingEggsStudentInfo();
waitForRequests("student");
getReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();
waitForRequests("student");

casper.run();
