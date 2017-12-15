var queue = new Limit(100);
studentRequests = new Requests();

//Grade position and class id lists are on the students page so we can use them
//to look up these values
studentRequests.lookupGradePosition = function(grade) {
  return $("#student_grade_position option:contains('" + grade + "')")
    .filter(function() { return ($(this).text() === grade); })
    .val();
};

studentRequests.lookupClassID = function(className) {
  return $("#student_school_class_id option:contains('" + className + "')")
    .filter(function() { return ($(this).text() === className); })
    .val();
};
      
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
    "student[grade_position]": this.lookupGradePosition(student.grade),
    "student[school_class_id]": this.lookupClassID(student.className),
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

studentRequests.del = function(ids) {
  var postData = {
    utf8: "",
    _method: "patch",
    authenticity_token: this.authenticity_token,
    school_class_id: "",
    operation: "delete",
    password: "",
    password_confirmation: "",
    grade_position: "", 
    "student_ids[]": ids 
  };
  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/student_body",
    data: postData,
    success: function(data) { studentRequests.delCallback(data, ids); }, 
    error: this.errorCallback
  };
      
  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
}

studentRequests.addCallback = function(data, student) {
  var $data;
  var id;
  var $tr;

  this.requestsRemaining--;
  console.log("Adding " + student.firstName + " " + student.lastName + ": " +
    this.parseInfo(data));
  //Adding is actually two steps: An add, then an edit to set login, password,
  //and studentID
  $data = $(data);
  $tr = $data.find("tr.student")
    .has("td.first_name:contains(" + student.firstName + ")")
    .has("td.last_name:contains(" + student.lastName + ")")
    .has("td.grade_name:contains(" + student.grade + ")")
    .has("td.teacher_names:contains(" + student.className + ")");
  if ($tr.length) {
    student.readingEggsID = $tr.attr("id").slice(8);
    this.edit(student);
  }
};

studentRequests.add = function(student) {
  var postData = {
    utf8: "",
    authenticity_token: this.authenticity_token,
    "student[first_name]": student.firstName,
    "student[last_name]": student.lastName,
    "student[grade_position]": this.lookupGradePosition(student.grade),
    "student[school_class_id]": this.lookupClassID(student.className)
  };
  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/students",
    data: postData,
    success: function(data) { studentRequests.addCallback(data, student); },
    error: this.errorCallback
  };

  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
};
