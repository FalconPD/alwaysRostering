var queue = new Limit(100);
teacherRequests = new Requests();

teacherRequests.loadCallback = function(data, teacher) {
      var $data

      this.requestsRemaining--;
      $data = $(data);
      teacher.login = $data.find("#teacher_login").val();
      teacher.firstName = $data.find("#teacher_first_name").val();
      teacher.lastName = $data.find("#teacher_last_name").val();
      teacher.email = $data.find("#teacher_email").val();
      teacher.password = $data.find("#teacher_password").val();
      teacher.passwordConfirmation = $data.find("#teacher_password_confirmation").val();
      teacher.accent = $data.find("#teacher_accent_id option:selected").val();
      teacher.receiveEmails = $data.find("#teacher_receive_mathseeds_emails").is(":checked");
};

teacherRequests.load = function() {
  $("#manage-entities tbody tr").each(function(index, element) {
    var teacher = {};
    var url;

    teacher.id = $(this).attr('id').slice(8);        
    teacher.students = $(this).children("td.students").text();
    teacher.trialEndDate = $(this).children("td.trial_end_date").text();
    teacherRequests.data.push(teacher);
    url = "https://app.readingeggs.com/re/school/teachers/" + teacher.id;
    teacherRequests.requestsRemaining++;
    queue.add($.get, url, function(data) {
      teacherRequests.loadCallback(data, teacher);
    });
  });
};

teacherRequests.editCallback = function(data, teacher) {
  this.requestsRemaining--;
  console.log("Editing " + teacher.firstName + " " + teacher.lastName + ": " +
    this.parseInfo(data));
}

teacherRequests.edit = function(teacher) {
  var postData = {
    utf8: "",
    _method: "patch",
    authenticity_token: this.authenticity_token,
    "teacher[login]": teacher.login,
    "teacher[first_name]": teacher.firstName,
    "teacher[last_name]": teacher.lastName,
    "teacher[email]": teacher.email,
    "teacher[password]": teacher.password,
    "teacher[password_confirmation]": teacher.password,
    "teacher[accent_id]": 3,
    "teacher[receive_mathseeds_emails]": 0,
    commit: "Update+Teacher"
  };
  var ajaxSettings = {
    type: "POST",
    url: "https://app.readingeggs.com/re/school/teachers?id=" +
      teacher.readingEggsID,
    data: postData,
    success: function(data) { teacherRequests.editCallback(data, teacher); }, 
    error: this.printError
  };

  this.requestsRemaining++;
  queue.add($.ajax, ajaxSettings);
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
};
