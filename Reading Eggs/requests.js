function Requests() {
  this.requestsRemaining = 0;
  this.authenticity_token = $("input[name='authenticity_token']:first").val();
  this.data = [];

  this.parseInfo = function parseInfo(data) {
    var $data;
    var error;
    var info;

    $data = $(data);
    error = $data.find("#flash_alert").text().replace(/\s\s+|\n/g, " ");
    info = $data.find("#flash_notice").text().replace(/\s\s+|\n/g, " ");

    return error + info;
  };

  this.printError = function printError(jqXHR, textStatus, errorThrown) {
    this.requestsRemaining--;
    console.log("Error " + errorThrown + " " + textStatus);
  };

  this.get = function() { return this.data; };
  this.done = function() { return (this.requestsRemaining === 0); };
}
