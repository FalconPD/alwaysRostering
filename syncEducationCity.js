"use strict";
/**********************************************************************/
/********************** syncEducationCity.js **************************/
/**********************************************************************/
/* This script uses the alwaysRostering framework to login to education
   city for the three schools that currently use it (BBS, OTS, MLS) and
   delete students that aren't in the alwaysRostering report, add students
   that are on the report, but aren't in EducationCity, update students
   that have different info (not including password), delete empty classes,
   add teachers that are on the report, and delete teachers that aren't
   on the report. */

/********************* Globals and Libraries **************************/
var educationCityStudentInfo;
var educationCityTeacherInfo;
var educationCityClassInfo;
var casper = require("casper").create({
  pageSettings: {
    loadImages: false,
    loadPlugins: false
  }
});
var utils = require("utils");
var alwaysRostering = require("./include/alwaysRostering");
var moment = require("./include/moment.min.js");

/******************* Utility Functions *******************************/
function lookupEducationCityStudent(studentID) {
  var i;

  for (i in educationCityStudentInfo) {
    if (educationCityStudentInfo[i].user_defined_id === studentID) {
      return educationCityStudentInfo[i];
    }
  }
  return false;
}

function lookupEducationCityTeacher(username) {
  var i; 

  for (i in educationCityTeacherInfo) {
    if (educationCityTeacherInfo[i].username === username) {
      return educationCityTeacherInfo[i];
    }
  }
  return false;
}

function lookupTeacherByUsername(username) {
  var teacherID;

  for (teacherID in alwaysRostering.teacherInfo) {
    if (username === alwaysRostering.teacherEmail(teacherID)) {
      return teacherID;
    }
  }
  return false;
}

function lookupEducationCityClass(title) {
  var i;

  for (i in educationCityClassInfo) {
    if ((educationCityClassInfo[i].type === "Class") &&
        (educationCityClassInfo[i].title === title)) {
      return educationCityClassInfo[i].id;
    }
  }
  return false;
}

//Deletes a group of users from EducationCity. Takes an array of EducationCity
//ids.
function deleteEducationCityUsers(users) {
  var deleteData = {"method": "delete", "data": {ids: "", type: 5}};
  var deleteCount = 0;

  users.forEach(function(user) {
    deleteData.data.ids += user + "-";
  });
  if (users.length > 0) {
    casper.echo("Submitting request to delete " + users.length + " users");
    alwaysRostering.jsonPost("https://ec2.educationcity.com/api/user/",
                             deleteData);
    if (! alwaysRostering.dryRun) {
      casper.then(function() {
        var response;
        var numberDeleted;

        response = JSON.parse(this.getPageContent());
        numberDeleted = Object.keys(response).length;
        if (numberDeleted !== users.length) {
          this.echo("Error in response:");
          this.echo(utils.dump(response));
          this.exit();
        }
        this.echo(numberDeleted + " users deleted from Education City");
      });
    }
  }
} 

/******************* Steps in Sync Process ***************************/
function login(username, password) {
  casper.then(function() {
    this.echo("Logging in as " + username + "...");
    casper.open("https://ec2.educationcity.com");
  });
  casper.then(function() {
    this.evaluate(function(username, password) {
      document.getElementById("username").value = username;
      document.getElementById("password").value = password;
      document.getElementById("login").click();
    }, username, password);
  }).waitForUrl("https://ec2.educationcity.com/home");
}

function logout() {
  casper.then(function() {
    this.echo("Logging out..."); 
    this.open("https://ec2.educationcity.com/user_management/logout/").waitForUrl("https://ec2.educationcity.com/");
  });
}

function loadEducationCityInfo(infoName) {
  casper.then(function() {
    this.echo("Loading " + infoName + " info from EducationCity...");
    switch (infoName) {
      case "students":
        this.open("https://ec2.educationcity.com/api/user/page/1/rp/1000/sortname/fullname/sortorder/asc/type/5/ignoreLive/false/groupByActiveStudents/true");
      break;
      case "teachers":
        this.open("https://ec2.educationcity.com/api/user/page/1/rp/1000/sortname/fullname/sortorder/asc/type/4/ignoreLive/false/groupByActiveStudents/true");
      break;
      case "classes":
        this.open("https://ec2.educationcity.com/api/group/type/1");
      break;
      default:
        this.echo("Unknown infoName in educationCityLoadInfo: " + infoName);
        this.exit();
    }
  });
  casper.then(function() {
    var count;
    var info;

    info = JSON.parse(this.getPageContent());
    if ("errors" in info) {
      this.echo("Error while fetching info: " + info.errors);
      this.exit();
    }
    count = Object.keys(info).length;
    this.echo("Loaded " + count + " " + infoName);
    switch (infoName) {
      case "students":
        educationCityStudentInfo = info;
      break;
      case "teachers":
        educationCityTeacherInfo = info;
      break;
      case "classes":
        educationCityClassInfo = info;
      break;
      default:
        this.echo("Unknown infoName in educationCityLoadInfo: " + infoName);
        this.exit();
    }
  });
}

function deleteStudents() {
  casper.then(function() {
    var i;
    var student;
    var students = [];

    this.echo("Determining which students to delete...");
    for (i in educationCityStudentInfo) {
      student = educationCityStudentInfo[i];        
      if (! (student.user_defined_id in alwaysRostering.studentInfo))
      {
        this.echo("[DELETE] " + student.user_defined_id + ": " +
                  student.firstname + " " + student.lastname);
        students.push(student.id);
      }
    }
    deleteEducationCityUsers(students);
  });
}

function deleteTeachers() {
  casper.then(function() {
    var i;
    var teacher;
    var teachers = [];

    this.echo("Determining which teachers to delete...");
    for (i in educationCityTeacherInfo) {
      teacher = educationCityTeacherInfo[i];
      if (! lookupTeacherByUsername(teacher.username)) {
        this.echo("[DELETE] " + teacher.title + " " + teacher.firstname + " " + 
                  teacher.lastname + " " + teacher.username);
        teachers.push(teacher.id);
      }
    }
    deleteEducationCityUsers(teachers);
  });
}

function addStudents() {
  casper.then(function() {
    var addData = {"data": [],
                   "user_type" : 5,
                   "commit": true,
                   "skip_warnings": true};
    var studentID;
    var addCount;

    this.echo("Determining which students to add...");
    for (studentID in alwaysRostering.studentInfo) {
      if (! lookupEducationCityStudent(studentID)) {
        alwaysRostering.studentMessage(studentID, "ADDING", "");
        addData["data"].push({
          "undefined": "",
          "user_defined_id": studentID,
          "first_name": alwaysRostering.studentInfo[studentID].firstName,
          "last_name": alwaysRostering.studentInfo[studentID].lastName,
          "class_name":
            alwaysRostering.studentInfo[studentID].homeroomTeacher,
          "username": alwaysRostering.elementaryUsername(studentID),
          "password": alwaysRostering.elementaryPassword(studentID),
          "gender": alwaysRostering.gender(studentID),
          "date_of_birth":
            alwaysRostering.studentInfo[studentID].dob,
          "academic_year": alwaysRostering.academicYear(studentID),
          "preserved_warnings": ""
        });
      }
    }
    addCount = addData.data.length;
    if (addCount > 0) { 
      this.echo("Submitting request to add " + addCount + " students");
      alwaysRostering.jsonPost("https://ec2.educationcity.com/api/bulk_user_management", addData);
      if (! alwaysRostering.dryRun) {
        casper.then(function() {
          var response;
          var numberAdded;

          response = JSON.parse(this.getPageContent());
          if (response.total_errors != 0) {
            this.echo("Errors detected in add students request response:");
            this.echo(utils.dump(response));
            this.exit();
          }
          numberAdded = Object.keys(response.data).length;
          this.echo(numberAdded + " students added to Education City");
        });
      }
    }
  });
}

function updateStudents() {
  casper.then(function() {
    var updateStudents = [];
    var addClasses = [];
    var i;
    var genesisStudent;
    var educationCityStudent;
    var comparisons = [];
    var needsUpdate;
    var title;

    this.echo("Determining which students to update...");
    for (studentID in alwaysRostering.studentInfo) {
      genesisStudent = alwaysRostering.studentInfo[studentID];
      educationCityStudent = lookupEducationCityStudent(studentID);
      if (educationCityStudent) {
        comparisons = [
          ["First Name",
           educationCityStudent.firstname, genesisStudent.firstName],
          ["Last Name",
           educationCityStudent.lastname, genesisStudent.lastName],
          ["Class Name",
           educationCityStudent.className, genesisStudent.homeroomTeacher],
          ["Username",
           educationCityStudent.username,
           alwaysRostering.elementaryUsername(studentID)],
          ["Gender",
           educationCityStudent.gender,
           alwaysRostering.gender(studentID)],
          ["Date of Birth",
           educationCityStudent.dob,
           moment(genesisStudent.dob, "M/D/YYYY").format("DD/MM/YYYY")],
          ["Academic Year",
           educationCityStudent.yearString,
           alwaysRostering.academicYear(studentID)]];
        needsUpdate = false;
        for (i = 0; i < comparisons.length; i++) {
          if (comparisons[i][1] != comparisons[i][2]) {
            alwaysRostering.studentMessage(studentID, "UPDATE",
              comparisons[i][0] + " does not match (" + comparisons[i][1] +
              "->" + comparisons[i][2] + ")");
            needsUpdate = true;
          }
        }
        if (needsUpdate) {
          //Check if we need to add the class as well
          title = genesisStudent['Homeroom Teacher'];
          if (addClasses.indexOf(title) === -1) {  
            if (! lookupEducationCityClass(title))
              addClasses.push(title);
          }    
          updateStudents.push(studentID);
        }
      }
    }
    casper.each(addClasses, function(self, title) {
      self.then(function() {
        var data = {
         "groupingName": title,
         "groupingNote": "",	
         "groupingId": 0,
         "groupingType":	"class"
        }

        this.echo("Creating class " + title + "...");
        alwaysRostering.post(
          "https://ec2.educationcity.com/user_management/saveGrouping/", data);
      });
      self.then(function() {
        response = JSON.parse(this.getPageContent());
        if (! response.success) {
          this.echo("Unable to add class: " + response.messages);
          this.exit();
        }
        this.echo(response.messages);
      });
    });
    if (addClasses.length > 0) {
      loadEducationCityInfo("classes");
    }
    casper.each(updateStudents, function(self, studentID) {
      self.then(function() {
        var data;

        this.echo("Updating student " + studentID + "...");
        genesisStudent = alwaysRostering.studentInfo[studentID];
        educationCityStudent = lookupEducationCityStudent(studentID);
        data = {
          "username": alwaysRostering.elementaryUsername(studentID),
          "password": educationCityStudent.password, //don't change the PW
          "firstname": genesisStudent.firstName,
          "lastname": genesisStudent.lastName,
          "title": null,
          "live": 1,
          "gender": alwaysRostering.gender(studentID),
          "classId": lookupEducationCityClass(genesisStudent.homeroomTeacher),
          "dob": moment(genesisStudent.dob, "M/D/YYYY")
                  .format("DD/MM/YYYY"),
          "year": (parseInt(genesisStudent.grade) + 3).toString(),  
          "typeId": 5,
          "id": educationCityStudent.id,
          "email": "",
          "role": null,
          "userSubjects": educationCityStudent.userSubjects,
          "userDefinedId": studentID
        }
        alwaysRostering.jsonPost("https://ec2.educationcity.com/api/user", data);
      });
      self.then(function() {
        var response;

        response = JSON.parse(this.getPageContent());
        if (! response.id) {
          this.echo("Unable to update student:");
          this.echo(utils.dump(response));
          this.exit();
        }
        else {
          this.echo("Student updated successfully.");
        }
      });
    });
    if (updateStudents.length > 0) {
      loadEducationCityInfo("classes");
    }
  });
}

function deleteEmptyClasses() {
  casper.then(function() {
    var i;
    var group;
    var request  = {
      method:	"delete",
      data: {
        ids: "",
        type: 1
      }
    };
    var delCount = 0; 

    this.echo("Determining which classes to delete..."); 
    for (i in educationCityClassInfo) {
      group = educationCityClassInfo[i];
      if ((group.type === "Class") && (group.active_students === 0)) {
        this.echo("[DELETING] Class: " + group.title);
        request.data += group.id + "-";
        delCount++;
      }
    }
    if (delCount > 0) {
      this.echo("Submitting request to delete " + delCount + " classes");
      alwaysRostering.jsonPost("https://ec2.educationcity.com/api/group/",
        request);
      if (! alwaysRostering.dryRun) {
        casper.then(function() {
          var response;

          response = JSON.parse(this.getPageContent());
          this.echo(Object.keys(response).length +
                    " classes deleted from Education City");
        });
      }
    }
  });  
}

//FYI: Teachers are added differently than students, but still have the same
//user objects once added
function addTeachers() {
  casper.then(function() {
    var data = {
      user_csv_data: "",
      user_type_id: "4",
    };
    var username;
    var teacherID;
    var teacher;
    var addCount = 0;
    var row;
    var title;

    this.echo("Determining which teachers to add...");
    for (teacherID in alwaysRostering.teacherInfo) {
      teacher = alwaysRostering.teacherInfo[teacherID];
      username = alwaysRostering.teacherEmail(teacherID);
      title = alwaysRostering.title(teacherID);
      row = [];
      if (! lookupEducationCityTeacher(username)) {
        this.echo("[ADDING] " + title + " " + teacher.firstName
                  + " " + teacher.lastName + " " + username);
        row.push(title);
        row.push(teacher.firstName);
        row.push(teacher.lastName);
        row.push(username);
        row.push(alwaysRostering.elementaryTeacherPassword(teacherID));
        row.push(username);
        data.user_csv_data += row.join(",") + "\n"; 
        addCount++;
      }
    }
    if (addCount > 0) {
      casper.then(function() {
        this.echo("Testing a request to add " + addCount + " teachers...");
        alwaysRostering.post("https://ec2.educationcity.com/user_management/validateUserList", data);
      });
      if (! alwaysRostering.dryRun) {
        casper.then(function() {
          var response;
          var key;

          response = JSON.parse(this.getPageContent());
          data.user_csv_data = "";
          data.save = 1;
          addCount = 0;
          response.forEach(function(row, index) {
            if ("warning4" in row) {
              casper.echo("Username already in use for " + row.col2 + " " +
                          row.col3 + ", not including in request");
              return;
            }
            if ("error1" in row) {
              casper.echo("Title missing for " + row.col2 + " " + row.col3 +
                          ", not including in request");
              return;
            }
            data.user_csv_data += row.col1 + "," + row.col2 + "," +
                                  row.col3 + "," + row.col4 + "," +
                                  row.col5 + "," + row.col6 + "\n";
            addCount++;
          });
        });
        casper.then(function() {
          if ((addCount > 0) && (! alwaysRostering.dryRun)){
            this.echo("Submitting a request to add " + addCount + " teachers...");
            alwaysRostering.post("https://ec2.educationcity.com/user_management/validateUserList", data);
            casper.then(function() {
              var response;

              response = JSON.parse(this.getPageContent());
              if (response.length != addCount) {
                this.echo("Unable to add all teachers");
                this.echo(utils.dump(response));
                this.exit();
              }
            });
          }
        });
      }
    }
  });
}

/***************************** Initialization ***************************/
alwaysRostering.init("syncEducationCity.js");

/***************************** Main Loop ******************************/
var schoolsAndGrades = [ { school: "MLS", grades: ["K", "1", "2", "3"] },
                         { school: "BBS", grades: ["K", "1", "2"] },
                         { school: "OTS", grades: ["K", "1", "2", "3" ] } ];
var grades;
var schools;
var username;
var password;

schoolsAndGrades.forEach(function(element) {
  casper.then(function() {
    grades = element.grades;
    schools = [element.school];
    username =
      alwaysRostering.credentials.educationCity[element.school].username;
    password =
      alwaysRostering.credentials.educationCity[element.school].password;

    alwaysRostering.loadStudentReport(casper.cli.args[0], grades, schools);
    alwaysRostering.loadTeacherReport(casper.cli.args[1], schools);
    login(username, password);
  });
  loadEducationCityInfo("students");
  deleteStudents();
  addStudents();
  loadEducationCityInfo("classes"); //need class info to update a student
  updateStudents();
  deleteEmptyClasses();
  loadEducationCityInfo("teachers");
  deleteTeachers();
  addTeachers();
  logout();
});

casper.run();
