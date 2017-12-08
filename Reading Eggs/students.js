var queue = new Limit(100);
studentRequests = new Requests();

studentRequests.loadCallback = function(data, student) {
      var $data

      this.requestsRemaining--;
      $data = $(data);
      student.firstName = $data.find("#student_first_name").val();
      student.lastName = $data.find("#student_last_name").val();
      student.gradePosition = $data.find(
        "#student_grade_position option:selected").val();
      student.schoolClassId = $data.find(
        '#student_school_class_id option:selected').val();
      student.login = $data.find("#student_login").val();
      student.password = $data.find("#student_password").val();
      student.passwordConfirmation = $data.find(
        "#student_password_confirmation").val();
      student.studentId = $data.find("#student_student_id").val();
};

studentRequests.load = function() {
  $("#manage-entities tbody tr.student").each(function(index, element) {
    var student = {};
    var url;

    student.id = $(this).attr('id').slice(8);        
    student.gradeName = $(this).children("td.grade_name").text();
    student.teacherNames = $(this).children("td.teacher_names").text();
    studentRequests.data.push(student);
    url = "https://app.readingeggs.com/re/school/students/" + student.id +
      "/edit";
    studentRequests.requestsRemaining++;
    queue.add($.get, url, function(data) {
      studentRequests.loadCallback(data, student);
    }); 
  });
};

studentRequests.editCallback = function(data, student) {
  this.requestsRemaining--;
  console.log("Editing " + student.firstName + " " + student.lastName + ": " +
    this.parseInfo(data));
};

studentRequests.edit = function(student) {
  var postData = {
    utf8: "",
    _method: "patch",
    authenticity_token: this.authenticity_token,
    "student[first_name]": student.firstName,
    "student[last_name]": student.lastName,
    //Grade position and class id lists are on the students page so
    //we can use them to look up these values
    "student[grade_position]":
      $("#student_grade_position option:contains('" + student.grade +
        "')").val(),
    "student[school_class_id]":
      $("#student_school_class_id option:contains('" + student.className +
        "')").val(),
    "student[login]": student.login,
    "student[password]": student.password,
    "student[password_confirmation]": student.password,
    "student[student_id]": student.studentID,
    commit: "Update+Student"
  }

  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/students/" +
      student.readingEggsID,
    data: postData,
    success: function(data) { studentRequests.editCallback(data, student); },
    error: this.errorCallback
  };
   
  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
};
/*
teacherRequests.delCallback = function(data, ids) {
  this.requestsRemaining--;
  console.log("Deleting " + ids + ": " + this.parseInfo(data));
}

teacherRequests.del = function(ids) {
  var postData = {
    utf8: "",
    _method: "patch",
    authenticity_token: this.authenticity_token,
    operation: "remove_teachers",
    "teacher_ids[]": ids 
  };
  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/teachers",
    data: postData,
    success: function(data) { teacherRequests.delCallback(data, ids); }, 
    error: this.errorCallback
  };
      
  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
}

teacherRequests.addCallback = function(data, teacher) {
  this.requestsRemaining--;
  console.log("Adding " + teacher.firstName + " " + teacher.lastName + ": " +
    this.parseInfo(data));
};

teacherRequests.add = function(teacher) {
  var postData = {
    utf8: "",
    "teacher[first_name]": teacher.firstName,
    "teacher[last_name]": teacher.lastName,
    "teacher[email]": teacher.email,
    "teacher[email_confirmation]": teacher.email,
    account_type: "no_trial",
    commit: "Create+Teacher"
  };
  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/teachers",
    data: postData,
    success: function(data) {
      teacherRequests.addCallback(data, teacher);
    },
    error: this.errorCallback
  };

  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
};*/
