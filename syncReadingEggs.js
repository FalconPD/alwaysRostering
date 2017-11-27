"use strict";

//TODO: Add dry-run checks

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

//Waits for the page to load, then prints the notification at the top of the
//page you get after submitting an edit for a teacher or student 
function printEditMessage(email) {

  casper.waitFor(
    function check() {
      return casper.evaluate(function() {
        return (document.getElementById("flash_alert") ||
                document.getElementById("flash_notice"));
      });
    },
    function then() {
      var message;

      message = casper.evaluate(function() {
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
      casper.echo(message);
    }
  );
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
    //TODO: Actually perform deletes
  });
}

//Same deal as students, we have to look on each edit screen to get all the
//info for a teacher. Does NOT load teacher data for a login passwed to it so
//we don't mess with the admin account
function loadReadingEggsTeacherInfo(adminLogin) {
  var timeout;

  casper.then(function() {
    this.echo("Loading teacher info from Reading Eggs...");
    this.open("https://app.readingeggs.com/re/school/teachers");
  });
  casper.then(function() {
    timeout = this.evaluate(function(adminLogin) {
      //Globals in the context of the page
      teachers = [];
      completed_teachers = 0;

      //Local to this evaluation
      var timeout = 0;
      var TIMEOUT_INTERVAL = 100;

      function parseEditPage(data, teacher) {
        var $data

        $data = $(data);
        teacher.login = $data.find("#teacher_login").val();
        teacher.email = $data.find("#teacher_email").val();
        teacher.password = $data.find("#teacher_password").val();
        teacher.passwordConfirmation =
          $data.find("#teacher_password_confirmation").val();
        teacher.accent = $data.find("#teacher_accent_id option:selected").val();
        teacher.receiveEmails =
          $data.find("#teacher_receive_mathseeds_emails").is(":checked");
        completed_teachers++;
      }

      $("#manage-entities tbody tr").each(function(index, element) {
        var teacher = {};

        teacher.login = $(this).children("td.login").text();
        if (teacher.login === adminLogin) { //don't load info for admin
          return;
        }
        teacher.id = $(this).attr('id').slice(8);        
        teacher.firstName = $(this).children("td.first_name").text();
        teacher.lastName = $(this).children("td.last_name").text();
        teacher.students = $(this).children("td.students").text();
        teacher.trialEndDate = $(this).children("td.trial_end_date").text();

        teachers.push(teacher);

        setTimeout(function() {
          $.get("https://app.readingeggs.com/re/school/teachers/" + teacher.id,
            function(data) {
              parseEditPage(data, teacher);
            }
          );
        }, timeout);
        timeout += TIMEOUT_INTERVAL;
      });
      return teachers.length * (TIMEOUT_INTERVAL * 2);
    }, adminLogin);
  });
  casper.then(function check() {
    casper.waitFor(function() {
      return this.evaluate(function() {
        return (completed_teachers === teachers.length);
      });
    }, function then() {
      readingEggsTeacherInfo = this.getGlobal("teachers");
    },
    function timeoutFunction() {
      this.echo("Timed out waiting for responses (" + timeout + " ms)");
      this.exit();
    }, timeout);
  });
}

//teachers have to be looked up by first and last name so the only thing
//we can really update is their login and email
function updateDeleteTeachers() {
  var updates = [];
  var deletes = [];

  casper.then(function() {
    readingEggsTeacherInfo.forEach(function(rTeacher) {
      var comparisons = [];
      var teacherID;
      var gTeacher;
      var gTeacherEmail;
      var needsUpdate = false;

      teacherID = alwaysRostering.lookupTeacher(rTeacher.firstName,
        rTeacher.lastName);
      if (teacherID) {
        gTeacher = alwaysRostering.teacherInfo[teacherID];
        gTeacherEmail = alwaysRostering.teacherEmail(teacherID);
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
          updates.push({rTeacher: rTeacher, teacherID: teacherID});
        }
      } else {
        casper.echo("[DELETE] " + rTeacher.firstName + " " + rTeacher.lastName);
        deletes.push(rTeacher.id);
      }
    });
    this.echo("Deletes: " + deletes.length + " Updates: " + updates.length);
    this.echo("Updating...");
    updates.forEach(function(element) {
      var email;
      var url;

      email = alwaysRostering.teacherEmail(element.teacherID);
      url = "https://app.readingeggs.com/re/school/teachers/" +
        element.rTeacher.id;
      casper.thenOpenAndEvaluate(url, function(email) {
        document.getElementById("teacher_login").value = email;
        document.getElementById("teacher_email").value = email;
        $("input[type=submit]").click();
      }, email);
      casper.then(function() {
        printEditMessage(email);
      });
    });
    //TODO: Actually do teacher deletes
  });
}

/************************* Initialization **********************************/
alwaysRostering.init("syncReadingEggs.js");

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
loadReadingEggsTeacherInfo(username);
updateDeleteTeachers();
loadReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();

casper.run();
