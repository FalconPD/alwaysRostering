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

function findTeachersToAdd() {
  var teacher = {};
  var teacherID;
  var email;
  var adds = [];

  for (teacherID in alwaysRostering.teacherInfo) {
    teacher = alwaysRostering.teacherInfo[teacherID];
    email = alwaysRostering.teacherEmail(teacherID);

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
      adds.push(teacherID);
    }
  }

  return adds;
}

//Waits for the page to load, then prints the notification at the top of the
//page you get after submitting an edit for a teacher or student 
function printEditMessage() {

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
    var studentID;

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
      casper.then(function() {
        printEditMessage();
      });
    });
    //TODO: Actually perform deletes
  });
}

function setupTeacherPage() {
  casper.then(function() {
    this.echo("Loading teacher info from Reading Eggs...");
    this.open("https://app.readingeggs.com/re/school/teachers");
  });

  //We need to inject the queue and teacher code to run our functions
  casper.thenEvaluate(alwaysRostering.ARQueue);
  casper.thenEvaluate(ARTeacher);
}

function loadReadingEggsTeacherInfo(adminLogin) {
  casper.thenEvaluate(function() { ARTeacher.load(); });
  casper.then(function() {
    casper.waitFor(
      function() {
        return casper.evaluate(function() {
          return ARTeacher.done();
        });
      },
      function then() {},
      function onTimeout() {
        casper.echo("Timed out loading teachers.");
        casper.exit();
      },
      60*2*1000 //Take up to two minutes to load all the teachers
    );
  });
  casper.then(function() {
    var i;

    readingEggsTeacherInfo = casper.evaluate(function() {
      return ARTeacher.getTeachers();
    });
    //don't touch the admin account
    for (i = 0; i < readingEggsTeacherInfo.length; i++) {
      if (readingEggsTeacherInfo[i].login === adminLogin) {
        readingEggsTeacherInfo.splice(i, 1);
      }
    }
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
        printEditMessage();
      });
    });
    //TODO: Actually do teacher deletes
  });
}

function addTeachers() {
  var adds = [];

  casper.then(function() {
    adds = findTeachersToAdd();
  });
  casper.then(function() {
    var waitTime = 20000;

    casper.evaluate(alwaysRostering.ARQueue);
    casper.evaluate(teacherCode);
    casper.waitFor(
      function() {
        return casper.evaluate(function() {
          return ARTeacher.done();
        });
      },
      function then() {},
      function onTimeout() {
        casper.echo("Timed out waiting " + waitTime + "ms to add " +
                    adds.length + " teachers");
        casper.exit();
      },
      waitTime
    );            
  });
}

/************************* Code to Inject in Page **************************/
function ARTeacher() {
  window.ARTeacher = (function() {
    var requestsRemaining = 0;
    var authenticity_token = $("input[name='authenticity_token']:first").val();
    var teachers = [];

    function errorCallback(jqXHR, textStatus, errorThrown) {
      requestsRemaining--;
      console.log("Error " + errorThrown + " " + textStatus);
    }

    //Parses the page returned to the callback and returns info / errors
    function getInfo(data) {
      var $data;
      var error;
      var info;

      $data = $(data);
      error = $data.find("#flash_alert").text().replace(/\s\s+|\n/g, " ");
      info = $data.find("#flash_notice").text().replace(/\s\s+|\n/g, " ");

      return error + info;
    }

    function addTeacherCallback(data, firstName, lastName, email) {
      requestsRemaining--;
      console.log("Adding " + firstName + " " + lastName + ": " +
        getInfo(data));
    }

    function delTeacherCallback(data, ids) {
      requestsRemaining--;
      console.log("Deleting " + ids + ": " + getInfo(data));
    }

    function editTeacherCallback(data, id, login, firstName, lastName, email,
      password) {
      requestsRemaining--;
      console.log("Editing " + firstName + " " + lastName + ": " +
        getInfo(data));
    }

    function loadCallback(data, teacher) {
      var $data

      requestsRemaining--;
      $data = $(data);
      teacher.login = $data.find("#teacher_login").val();
      teacher.email = $data.find("#teacher_email").val();
      teacher.password = $data.find("#teacher_password").val();
      teacher.passwordConfirmation =
        $data.find("#teacher_password_confirmation").val();
      teacher.accent = $data.find("#teacher_accent_id option:selected").val();
      teacher.receiveEmails =
        $data.find("#teacher_receive_mathseeds_emails").is(":checked");
    }

    return {
      add: function(firstName, lastName, email) {
        var postData = {
          utf8:                          "",
          "teacher[first_name]":         firstName,
          "teacher[last_name]":          lastName,
          "teacher[email]":              email,
          "teacher[email_confirmation]": email,
          account_type:                  "no_trial",
          commit:                        "Create+Teacher"
        };
        var ajaxSettings = {
          type: "POST",
          url: "https://app.readingeggs.com/re/school/teachers",
          data: postData,
          success: function(data) {
            addTeacherCallback(data, firstName, lastName, email)
          },
          error: errorCallback
        };

        requestsRemaining++;
        ARQueue($.ajax, ajaxSettings);
      },
      del: function(ids) {
        var postData = {
          utf8:               "",
          _method:            "patch",
          authenticity_token: authenticity_token,
          operation:          "remove_teachers",
          "teacher_ids[]":    ids 
        };
        var ajaxSettings = {
          type: "POST",
          url: "https://app.readingeggs.com/re/school/teachers",
          data: postData,
          success: function(data) {
            delTeacherCallback(data, ids);
          }, 
          error: errorCallback
        };
      
        requestsRemaining++;
        ARQueue($.ajax, ajaxSettings);
      },
      edit: function(id, login, firstName, lastName, email, password) {
        var postData = {
          utf8:                                "",
          _method:                             "patch",
          authenticity_token:                  authenticity_token,
          "teacher[login]":                    login,
          "teacher[first_name]":               firstName,
          "teacher[last_name]":                lastName,
          "teacher[email]":                    email,
          "teacher[password]":                 password,
          "teacher[password_confirmation]":    password,
          "teacher[accent_id]":                3,
          "teacher[receive_mathseeds_emails]": 0,
          commit:                              "Update+Teacher"
        };
        var ajaxSettings = {
          type: "POST",
          url: "https://app.readingeggs.com/re/school/teachers?id=" + id,
          data: postData,
          success: function(data) {
            editTeacherCallback(data, id, login, firstName, lastName, email,
              password);
          }, 
          error: errorCallback
        };

        requestsRemaining++;
        ARQueue($.ajax, ajaxSettings);
      },
      load: function() {
        $("#manage-entities tbody tr").each(function(index, element) {
          var teacher = {};
          var url;

          teacher.login = $(this).children("td.login").text();
          teacher.id = $(this).attr('id').slice(8);        
          teacher.firstName = $(this).children("td.first_name").text();
          teacher.lastName = $(this).children("td.last_name").text();
          teacher.students = $(this).children("td.students").text();
          teacher.trialEndDate = $(this).children("td.trial_end_date").text();
          teachers.push(teacher);
          url = "https://app.readingeggs.com/re/school/teachers/" + teacher.id;
          requestsRemaining++;
          ARQueue($.get, url, function(data) { loadCallback(data, teacher); });
        });
      },
      getTeachers: function() {
        return teachers;
      },
      done: function() {
        return (requestsRemaining === 0);
      }
    }
  })();
}

/************************* Initialization **********************************/
alwaysRostering.init("syncReadingEggs.js");

/************************* Main Loop ***************************************/
var username;
var password;

alwaysRostering.loadStudentReport(["KF", "KH", "1", "2"], ["MLS"]);
alwaysRostering.loadTeacherReport(["MLS"], ["KF", "KH", "1", "2"]);
alwaysRostering.addTeacher("8016");
alwaysRostering.addHRTeacherStudents("WES", "8016");
username = alwaysRostering.credentials.readingEggs["MLS"].username;
password = alwaysRostering.credentials.readingEggs["MLS"].password;
login(username, password);
setupTeacherPage();
loadReadingEggsTeacherInfo(username);
/*updateDeleteTeachers();
addTeachers();
loadReadingEggsStudentInfo();
updateDeleteStudents();
addStudents();*/

casper.run();
