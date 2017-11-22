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
    function timeoutFunction() {
      this.echo("Timed out waiting for responses (" + timeout + " ms)");
      this.exit();
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
    var deletes = [];
    var updates = [];

    readingEggsStudentInfo.forEach(function(rstudent) {
      var studentID;
      var gstudent;
      var comparisons = [];
    
      studentID = rstudent.studentId;
      if (studentID === "") {
        studentID = alwaysRostering.lookupStudent(rstudent.firstName,
                                                  rstudent.lastName);
        if (studentID) {
          alwaysRostering.studentMessage(studentID, "UPDATE",
                                         "needs studentId added");
          updates.push({rstudent: rstudent, studentID: studentID});
        } else {
          casper.echo("[DELETE] " + rstudent.firstName + " " +
                      rstudent.lastName +
                      " does not have studentId, could not look up");
          deletes.push(rstudent.id);
        }
        return;
      }
      if (studentID in alwaysRostering.studentInfo) {
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
          updates.push({rstudent: rstudent, studentID: studentID});
        }
      } else {
        casper.echo("[DELETE] " + rstudent.studentId + ": " + rstudent.firstName
                    + " " + rstudent.lastName);
        deletes.push(rstudent.id);
      }
    });
    this.echo("Deletes: " + deletes.length + " Updates: " + updates.length);
    this.echo("Updating...");
    updates.forEach(function(element) {
      var url;
      var rstudent;
      var gstudent;
      var studentID;
      var firstName;
      var lastName;
      var login;
      var grade;
      var teacher;

      studentID = element.studentID;
      rstudent = element.rstudent;
      gstudent = alwaysRostering.studentInfo[studentID];
      firstName = gstudent.firstName;
      lastName = gstudent.lastName;
      login = alwaysRostering.elementaryUsername(studentID);
      teacher = alwaysRostering.hrTeacherFirstLast(studentID);
      grade = alwaysRostering.basicGrade(studentID);
      url = "https://app.readingeggs.com/re/school/students/" + rstudent.id +
            "/edit";
      casper.thenOpenAndEvaluate(url, function(firstName, lastName, login,
        studentID, teacher, grade) {
          document.getElementById("student_first_name").value = firstName;
          document.getElementById("student_last_name").value = lastName;
          document.getElementById("student_login").value = login;
          document.getElementById("student_student_id").value = studentID;
          $("#student_school_class_id option:contains('" + teacher +
            "')").prop("selected", "selected");
          $("#student_grade_position option:contains('" + grade +
            "')").prop("selected", "selected");
          $("input[type=submit]").click();
        }, firstName, lastName, login, studentID, teacher, grade);
      casper.waitForUrl("https://app.readingeggs.com/re/school/students",
        function()
      {
        var message;

        message = this.evaluate(function() {
          var error_div;
          var info_div;

          error_div = document.getElementById("flash_alert");
          info_div = document.getElementById("flash_notice");
          if (error_div) {
            return error_div.innerHTML;
          } else {
            return info_div.innerHTML;
          } 
        });
        this.echo(message);
      });
    });
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

alwaysRostering.loadStudentReport(["KF", "KH", "1", "2"], ["MLS"]);
alwaysRostering.loadTeacherReport(["MLS"]);
alwaysRostering.addTeacher("8016");
alwaysRostering.addHRTeacherStudents("WES", "8016");
username = alwaysRostering.credentials.readingEggs["MLS"].username;
password = alwaysRostering.credentials.readingEggs["MLS"].password;
login(username, password);
//TODO: Do teacher syncing first so the teachers are available when updating
//students
loadReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();

casper.run();
