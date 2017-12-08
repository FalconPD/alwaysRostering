//This prototype is meant to be injected in remote DOM 
//It sets up an object that runs functions sent to it with a delay between them
//USAGE: Limit(delay in ms), Limit.add(function to run, arguments...)
function Limit(delay) {
  this.last = 0;
  this.delay = delay;

  this.add = function(fn) {
    var now;
    var args = [];
    var i;

    //Remove the first argument, it is our callback function
    for (i = 0; i < arguments.length; i++) {
      if (i !== 0) {
        args.push(arguments[i]);
      }
    }

    now = new Date().getTime();
    if ((now - this.last) > this.delay) { //Run right away
      this.last = now;
      fn.apply(this, args);
    } else { //Run after a delay
      this.last += this.delay;
      setTimeout(function() { fn.apply(this, args) }, this.last - now);
    }
  }
}
