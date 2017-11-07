"use strict";

/**************************** Globals and Libraries ************************/
var casper = require("casper").create({
//  verbose: true,
//  logLevel: "debug",
  pageSettings: {
    loadImages: false,
    loadPlugins: false
  }
});
var utils = require("utils");
var alwaysRostering = require("./include/alwaysRostering");
var readingEggsStudentInfo = [];

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
  var timeout;

  casper.then(function() {
    this.echo("Loading student info from Reading Eggs...");
    this.open("https://app.readingeggs.com/re/school/students");
  });
//The main table has some information, but we also need to open the edit
//page to get more info. This is handled by a jquery get requests in the JS we
//evaluate. We estimate the max time it takes for a response to come in as twice
//the interval in between the requests we send 
  casper.then(function() {
    timeout = this.evaluate(function() {
      var TIMEOUT_INTERVAL = 100;
      students = [];
      completed_students = 0;
      var timeout = 0;
      
      function parseEditPage(data, student) {
        var $data;

        $data = $(data); //jquerify the html we got back
        student.gradePosition = $data.find('#student_grade_position option:selected').val();
        student.schoolClassId = $data.find('#student_school_class_id option:selected').val();
        student.password = $data.find('#student_password').val();
        student.passwordConfirmation = $data.find('#student_password_confirmation').val();
        student.studentId = $data.find('#student_student_id').val();

        completed_students++;
      }

      $("#manage-entities tbody tr.student").each(function(index, element) {
        var student = {};
        var url = "https://app.readingeggs.com/re/school/students";

        student.id = $(this).attr('id').slice(8);        
        student.firstName = $(this).children("td.first_name").text();
        student.lastName = $(this).children("td.last_name").text();
        student.login = $(this).children("td.login").text();
        student.gradeName = $(this).children("td.grade_name").text();
        student.teacherNames = $(this).children("td.teacher_names").text();

        students.push(student);
        setTimeout(function() {
          $.get(url + "/" + student.id + "/edit", function(data) {
            parseEditPage(data, student);
          });
        }, timeout);
        timeout += TIMEOUT_INTERVAL;
      });
      return students.length * (TIMEOUT_INTERVAL * 2);
    });
  });
  casper.then(function check() {
    casper.waitFor(function() {
      return this.evaluate(function() {
        return (completed_students === students.length);
      });
    }, function then() {
      readingEggsStudentInfo = this.evaluate(function() {
        return students;
      });
    },
    function timeout() {
      this.echo("Timed out waiting for responses (" + timeout + " ms)");
    }, timeout);
  });
}

function addStudents() {
  casper.then(function() {
    var adds = 0;
    var student = {};

    for (studentID in alwaysRostering.studentInfo) {
      student = alwaysRostering.studentInfo[studentID];
      if (! lookupReadingEggsStudent(studentID)) {
       alwaysRostering.studentMessage(studentID, "ADD", ""); 
       adds++;
      }
    }
    this.echo("Adds: " + adds);
  });
}

function updateDeleteStudents() {
  casper.then(function() {
    var deletes = 0;
    var updates = 0;

    readingEggsStudentInfo.forEach(function(rstudent) {
      var studentID;
      var gstudent;
      var comparisons = [];
    
      studentID = rstudent.studentId;
      if (studentID === "") {
        casper.echo("[DELETE] " + rstudent.firstName + " " + rstudent.lastName +
                    " (does not have studentId)");
        deletes++;
        return;
      }
      if (studentID in alwaysRostering.studentInfo) {
        gstudent = alwaysRostering.studentInfo[studentID];
        /*comparisons = [
          ["First Name", rstudent.firstName, gstudent.firstName],
          ["Last Name", rstudent.lastName, gstudent.lastName],
          ["Grade", rstudent.gradeName, gstudent.grade],
          ["Login", rstudent.login, gstudent.elementaryUserName(studentID)],
          ["Class Name", rstudent.teacherNames, gstudent.homeroomTeacher]
        ];*/
        updates++;
      } else {
        casper.echo("[DELETE] " + rstudent.studentId + ": " + rstudent.firstName
                    + " " + rstudent.lastName);
        deletes++;
      }
    });
  this.echo("Deletes: " + deletes + " Updates: " + updates);
  });
}

/************************* Initialization **********************************/
alwaysRostering.init("syncReadingEggs.js");
casper.on('remote.message', function(message) {
    this.echo("remote.message: " + message);
});
casper.on("page.error", function(msg, trace) {
    this.echo("page.error: " + msg);
});

/************************* Main Loop ***************************************/
var username;
var password;

alwaysRostering.loadStudentReport(["K", "1", "2", "3"], ["MLS"]);
alwaysRostering.loadTeacherReport(["MLS"]);
username = alwaysRostering.credentials.readingEggs["MLS"].username;
password = alwaysRostering.credentials.readingEggs["MLS"].password;
login(username, password);
loadReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();

casper.run();
