"use strict";

var Papa = require("../../include/papaparse");
var require = patchRequire(require);
var fs = require("fs");
var utils = require("utils");
var roster = [];

//Load all the teachers and the schools
alwaysRostering.loadTeacherReport([], []);
alwaysRostering.loadSchoolReport();

function addLine(teacher, student, className) {
  var teacherEmail;
  var studentEmail;
  var schoolInfo;
  var line;
  
  if (! (student.schoolCode in alwaysRostering.schoolInfo)) {
    casper.echo("addLine: Unable to lookup info for school code " +
      student.schoolCode);
    casper.exit();
  }

  schoolInfo = alwaysRostering.schoolInfo[student.schoolCode];
  teacherEmail = alwaysRostering.teacherEmail(teacher.id);
  studentEmail = alwaysRostering.studentEmail(student.id);
  if (studentEmail === "") {
    casper.echo("Warning: Could not create email for " + student.id);
  }
  line = {
    "School State Code": schoolInfo.stateSchoolCode,
    "School Name": schoolInfo.schoolName,
    "Previous Instructor ID": "",
    "Instructor ID": teacher.id,
    "Instructor State ID": teacher.stateID,
    "Instructor Last Name": teacher.lastName,
    "Instructor First Name": teacher.firstName,
    "Instructor Middle Initial": teacher.middleName,
    "User Name": teacherEmail,
    "Email Address": teacherEmail,
    "Class Name": className, 
    "Previous Student ID": "",
    "Student ID": student.id,
    "Student State ID": student.stateID,
    "Student Last Name": student.lastName,
    "Student First Name": student.firstName, 
    "Student Middle Initial": student.middleName,
    "Student Date Of Birth": student.dob,
    "Student Gender": student.genderCode,
    "Student Grade": student.grade,
    "Student Ethnic Group Name": student.ethnicity,
    "Student User Name": studentEmail,
    "Student Email": studentEmail
  };
  roster.push(line);
}
 
function rosterK3() {
  //Students K-3 don't have classes in Genesis so we have to go through each
  //student and roster them with the HR teacher

  var student;
  var teacher;
  var teacher1;
  var teacher2;
  var line;
  var teacherID;
  var className;
  var searchTeacher;
  var studentID;

  casper.echo("Rostering students K-3...");
  alwaysRostering.loadStudentReport(["OTS", "BBS", "BES", "MLS"], ["KF", "KH",
    "SC1", "SC2", "SC3", "1", "2", "3"]);

  for (studentID in alwaysRostering.studentInfo) {
    student = alwaysRostering.studentInfo[studentID];
    if (student.hrTeacherID === "") {
      alwaysRostering.studentMessage(studentID, "SKIP", "No HR teacher");
      continue;
    }
    teacher = alwaysRostering.teacherInfo[student.hrTeacherID];
    className = teacher.firstName + " " + teacher.lastName;
    if (teacher.half !== "") {
      className += " " + teacher.half;
      if (teacher.sharedTeacher !== "Y") { //Shared half teachers should already
                                           //link to the correct teachers
        //for half teachers, find the entry with a stateID in it
        if (teacher.stateID === "") {
          for (teacherID in alwaysRostering.teacherInfo) {
            searchTeacher = alwaysRostering.teacherInfo[teacherID];
            if ((searchTeacher.firstName === teacher.firstName) &&
                (searchTeacher.lastName === teacher.lastName) &&
                (searchTeacher.stateID !== ""))
            {
              teacher = searchTeacher;
            }
          }
        }
      }
    }
    if (teacher.sharedTeacher === "Y") {
      if (! (teacher.sharedTeacherID1 in alwaysRostering.teacherInfo)) {
        casper.echo("Warning: Unable to find teacher " +
          teacher.sharedTeacherID1 + " referenced by shared teacher " +
          teacher.id);
      }
      else
      { 
        teacher1 = alwaysRostering.teacherInfo[teacher.sharedTeacherID1];
        addLine(teacher1, student, className);
      }
      if (! (teacher.sharedTeacherID2 in alwaysRostering.teacherInfo)) {
        casper.echo("Warning: Unable to find teacher " +
          teacher.sharedTeacherID2 + " referenced by shared teacher " +
          teacher.id);
      }
      else
      { 
        teacher2 = alwaysRostering.teacherInfo[teacher.sharedTeacherID2];
        addLine(teacher2, student, className);
      }
    }
    else {
      addLine(teacher, student, className);
    }
  }
};

function roster48() {
  //These students have classes in Genesis. We pull from certain classes to
  //create our roster. We use a hash to store students and teachers
  //in a given gradebook courseID and then generate flat output from the hash.
  //This has the effect of merging rosters.
  var classes = {
    AMS: [
      "105", //Accelerated Math
      "110", //Algebra I
      "111", //Accelerated Algebra I
      "120", //Geometry
      "160", //Mathematics - Sixth Grade
      "170", //Mathematics - Seventh Grade
      "180", //Mathematics - Eight Grade
      "260", //Language Arts - Sixth Grade
      "270", //Language Arts - Seventh Grade
      "280"  //Language Arts - Eight Grade
    ],
    AES: [
      "140", //Mathematics
      "150", //Mathematics
      "159", //Accelerated Math
      "201", //Wilson Reading
      "240", //English Language Arts
      "250", //English Language Arts
    ],
    BES: [
      "140", //Mathematics
      "150", //Mathematics
      "159", //Accelerated Math
      "240", //English Language Arts
      "250", //English Language Arts
    ],
    WES: [
      "140", //Mathematics
      "150", //Mathematics
      "159", //Accelerated Math
      "240", //English Language Arts
      "250", //English Language Arts
    ]
  };
  var mergeHash = {};
  var courseID;
  var teachers;
  var students;
  var teacherID;
  var className;
  var teacher;
  var student;

  casper.echo("Rostering students 4-8...");
  alwaysRostering.loadStudentReport(["BES", "AES", "WES", "AMS"],
    ["4", "5", "6", "7", "8"]);
  alwaysRostering.loadClassReport(["BES", "AES", "WES", "AMS"]);

  alwaysRostering.classInfo.forEach(function(line) {
    if (classes[line.schoolCode].indexOf(line.courseCode) !== -1) {
      teacherID = line.teacherID;
      if (! (teacherID in alwaysRostering.teacherInfo)) {
        casper.echo("Warning: Unable to look up teacher " + teacherID);
        return;
      }
      studentID = line.studentID;
      if (! (studentID in alwaysRostering.studentInfo)) {
        casper.echo("Warning: Unable to look up student " + studentID);
        return;
      }
      courseID = line.gradebookCourseID;
      if (courseID === "") {
        casper.echo("Warning: No gradebookCourseID for this line");
        casper.echo(JSON.stringify(line));
        return
      }
      if (! (courseID in mergeHash)) {
        mergeHash[courseID] = {
          teachers: [],
          students: [],
          className: "Period " + line.printPeriods + " " +
            line.courseDescription + " (" + courseID + ")"
        };
      }
      teachers = mergeHash[courseID].teachers;
      students = mergeHash[courseID].students;
      if (teachers.indexOf(teacherID) === -1) {
        teachers.push(teacherID);
      }
      if (students.indexOf(studentID) === -1) {
        students.push(studentID);
      }
    }
  });

  for (courseID in mergeHash) {
    teachers = mergeHash[courseID].teachers;
    students = mergeHash[courseID].students;
    className = mergeHash[courseID].className;
    teachers.forEach(function(teacherID) {
      teacher = alwaysRostering.teacherInfo[teacherID];
      students.forEach(function(studentID) {
        student = alwaysRostering.studentInfo[studentID];
        addLine(teacher, student, className);
      });
    });
  }
}

function checkMaxClassSize(size) {
  var classes = {};
  var key;
  var school;
  var className;
  var teacherID
  var passed = true;

  roster.forEach(function(line) {
    school = line["School Name"];
    teacherID = line["Instructor ID"];
    className = line["Class Name"];
    key = "School: " + school + " Teacher: " + teacherID + " Class Name: " +
      className;
    if (key in classes) {
      classes[key]++;
    } else {
      classes[key] = 1;
    }
  });
  for (key in classes) {
    if (classes[key] > size) {
      casper.echo("Warning: " + key + " has " + classes[key] +
        " students.");
      passed = false;
    }
  }
  return passed;
};

function checkMaxCourseForStudent(courses) {
  var studentID;
  var students = {};
  var passed = true;

  roster.forEach(function(line) {
    studentID = line["Student ID"];
    students[studentID] ? students[studentID]++ : students[studentID] = 1;
  });
  for (studentID in students) {
    if (students[studentID] > courses) {
      casper.echo("Warning: Student " + studentID + " is in " +
        students[studentID] + " classes.");
      passed = false;
    }
  }
  return passed;
};

exports.getRoster = function() {
  return roster;
};

exports.sort = function() {
  roster.sort(function(a, b) {
    var comparisons = ["School Name", "Instructor Last Name", "Class Name",
      "Student Last Name", "Student First Name", "Student ID"];
    var i;
    var key;
    var result;

    for (i = 0; i < comparisons.length; i++) {
      key = comparisons[i];
      
      result = a[key].localeCompare(b[key]);
      if (result !== 0) {
        return result;
      }
    }
    casper.echo("Warning: Duplicate lines in roster");
    casper.echo(JSON.stringify(a));
    casper.echo(JSON.stringify(b));
    return 0;
  });
};
  
exports.write = function(name) {
  var csv;

  csv = Papa.unparse(roster);
  fs.write(name, csv, "w");
};

exports.check = function() {
  //Consider classes over 35 students suspicious
  checkMaxClassSize(35);

  //At most a student could be in 4 courses (2 subjects x 2 teachers)
  checkMaxCourseForStudent(4);
};

exports.create = function() {
  rosterK3();
  roster48();
};
