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
var alwaysRostering = require("../include/alwaysRostering");
var readingEggsStudentInfo = [];
var readingEggsTeacherInfo = [];

/*************************** Utility Functions *****************************/
function removeDuplicates(arr) {
    var unique_array = [];
    var i;

    for(i = 0; i < arr.length; i++) {
        if(unique_array.indexOf(arr[i]) == -1){
            unique_array.push(arr[i])
        }
    }
    return unique_array
}

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

function waitForRequests() {
  casper.then(function() {
    casper.waitFor(
      function() {
        return casper.evaluate(function() {
          if (typeof teacherRequests === "object") {
            return teacherRequests.done();
          }
          else {
            return studentRequests.done();
          }
        });
      },
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
      var grade;
    
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
        grade = alwaysRostering.basicGrade(studentID);
        if (parseInt(grade) > 9) { //Reading Eggs has a maximum grade of 9
          grade = rstudent.gradeName;
        } 
        comparisons = [
          ["First Name", rstudent.firstName, gstudent.firstName],
          ["Last Name", rstudent.lastName, gstudent.lastName],
          ["Grade", rstudent.gradeName, grade],
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
    if (deletes.length !== 0) {
      if (alwaysRostering.dryRun) {
        casper.echo("Dry run option set, not deleting.");
      } else {
        casper.evaluate(function(deletes) {
          studentRequests.del(deletes);
        }, deletes);
      }
    }
  });
}

function addStudents() {
  casper.then(function() {
    var student = {};
    var studentID;
    var addInfo;
    var grade;

    for (studentID in alwaysRostering.studentInfo) {
      student = alwaysRostering.studentInfo[studentID];
      if (! lookupReadingEggsStudent(studentID)) {
        alwaysRostering.studentMessage(studentID, "ADD", ""); 
        if (alwaysRostering.dryRun) {
          casper.echo("Dry run option set, not adding.");
        } else {
          grade = alwaysRostering.basicGrade(studentID);
          if (parseInt(grade) > 9) { //Reading Eggs has a maximum grade of 9
            grade = "9";
          }
          addInfo = {
            firstName: student.firstName,
            lastName: student.lastName,
            grade: grade,
            className: alwaysRostering.hrTeacherFirstLast(studentID),
            login: alwaysRostering.elementaryUsername(studentID),
            password: alwaysRostering.elementaryPassword(studentID),
            studentID: studentID
          }
          casper.evaluate(function(addInfo) {
            studentRequests.add(addInfo);
          }, addInfo);
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
var studentIDs;

//Barclay Brook - All K-2 students and teachers
alwaysRostering.loadStudentReport(["KF", "KH", "1", "2"], ["BBS"]);
alwaysRostering.loadTeacherReport(["BBS"], ["KF", "KH", "1", "2"]);

//Add Reading Specialist and students
//This particular teacher requested a list of students and needs them linked
//to her in ReadingEggs instead of their regular HR teacher
alwaysRostering.addTeacher("BES", "525");
studentIDs = ["92462", "87707", "88314", "87545", "87547", "88530", "90687",
  "87510", "91550", "92434", "89050", "92432", "88459", "89135", "89035",
  "89113", "89324", "89351", "92410", "88416"];
alwaysRostering.addStudents(studentIDs);
studentIDs.forEach(function(studentID) {
  alwaysRostering.studentInfo[studentID].hrTeacherID = "525"; 
});

//Add teacher of the Handicapped and students
alwaysRostering.addTeacher("BES", "562");
alwaysRostering.addHRTeacherStudents("BES", "562");

//Add HS inclusion teacher
alwaysRostering.addTeacher("MTHS", "2");
//get unique students from all the teacher's classes
alwaysRostering.loadClassReport(["MTHS"]); //need class data for this
studentIDs = removeDuplicates(
  alwaysRostering.studentsInClass("MTHS", "1700", "1")
  .concat(alwaysRostering.studentsInClass("MTHS", "1700", "2"))
  .concat(alwaysRostering.studentsInClass("MTHS", "1701", "1"))
  .concat(alwaysRostering.studentsInClass("MTHS", "1701", "2"))
  .concat(alwaysRostering.studentsInClass("MTHS", "1702", "1"))
  .concat(alwaysRostering.studentsInClass("MTHS", "1702", "2"))
);
//Add them and set the teacher as their HR teacher
alwaysRostering.addStudents(studentIDs);
studentIDs.forEach(function(studentID) {
  alwaysRostering.studentInfo[studentID].hrTeacherID = "2"; 
});

//Add Special Ed teacher and students
alwaysRostering.addTeacher("BBS", "434");
alwaysRostering.addHRTeacherStudents("BBS", "434");

//Add BES teacher who requested addition of one of her students
alwaysRostering.addTeacher("BES", "593");
alwaysRostering.addStudents(["88311"]);

username = alwaysRostering.credentials.readingEggs["BBS"].username;
password = alwaysRostering.credentials.readingEggs["BBS"].password;

login(username, password);
setupTeacherPage();
loadReadingEggsTeacherInfo();
waitForRequests();
getReadingEggsTeacherInfo();
ignoreAdminAccount(username);
updateDeleteTeachers();
addTeachers();
waitForRequests();
setupStudentPage();
loadReadingEggsStudentInfo();
waitForRequests();
getReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();
waitForRequests();

casper.run();
/*
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
*/

