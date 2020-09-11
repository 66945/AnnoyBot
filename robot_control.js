//constants for key codes
var DEL=8;
var ENTER=13;
var ESC=27;
var SPACE=32;
var PAGEUP=33;
var PAGEDOWN=34;
var END=35;
var HOME=36;
var LEFT=37;
var UP=38;
var RIGHT=39;
var DOWN=40;
var S_KEY=83;

var REPEAT_CMD_INTERVAL=5000; // Commands are resent every 5 seconds.

var xhttp=new XMLHttpRequest();

//===============================================================
// setSessionPassword
// Checks the URL for parameters that define session and user
// password, and if found then assign these values to the session
// and user password text fields.
//===============================================================
function setSessionPassword(){
  var session_field=document.getElementById("session");
  var password_field=document.getElementById("user_password");
  var url_param=document.URL.toString();

  if(url_param.indexOf('?')>0)url_param=url_param.split('?')[1];
  if(/session=(\d+)/.test(url_param))
    session_field.value=url_param.replace(/.*session=(\d+).*/,"$1");
  if(/user_password=(\d+)/.test(url_param))
    password_field.value=url_param.replace(/.*user_password=(\d+).*/,"$1");
}


//===============================================================
// callRepeatCommand
// Calls the serverLink.repeatCommand() method.
// This function is needed because the the interval timer cannot
// call methods directly.
//===============================================================
function callRepeatCommand(){
  serverLink.repeatCommand();
}

//===========================================================================
// ServerLink
// Handles sending commands to robot server.
//===========================================================================
function ServerLink(){
  this.command="stop";   // Robot is initially stopped.
  this.type="drive";
  this.interval=REPEAT_CMD_INTERVAL;
  this.lastCmdTime = new Date();
  this.cmdComplete = false;  // TRUE if response recieved from server.
  this.suspend=false;        // TRUE if repeat commands should not be sent.
}

ServerLink.prototype.sendCommand = function(command, type){
  this.cmdComplete=false;
  this.command = command;
  this.type = type;
  var session=document.getElementById('session').value;
  var user_password=document.getElementById('user_password').value;
  if(type=="drive"){
  	var quantity=document.getElementById('ds').value;
  }else if(type=="claw"){
  	var quantity=document.getElementById('cs').value;
  }else{
	  var quantity=0;
  }
  var status_display=document.getElementById('status');

  if(command=="suspend"){
    this.suspend=true;
    status_display.innerHTML="Commands suspended.";
  }else{
    this.suspend=false;
    xhttp.open("POST", "robot.php", false);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var request_string="request=send_command" +
                       "&session=" + session +
  	               "&user_password=" + user_password +
	               "&command=" + command +
	               "&quantity=" + quantity;
    xhttp.send(request_string);
    status_display.innerHTML=
      "Command:  " + command + " " + quantity + "   " + xhttp.statusText + 
      "<br>Response:  " + xhttp.responseText;
    this.lastCmdTime=new Date();
    this.cmdComplete=true;
  }
}

ServerLink.prototype.repeatCommand = function(){
  var now=new Date();
  if(this.cmdComplete && !this.suspend &&
     (now.getTime() - this.lastCmdTime.getTime() > this.interval)){
    this.sendCommand(this.command, this.type);
  }
}

ServerLink.prototype.startTimer = function(interval){
  if(interval > 0)this.interval=interval;
  // Check whether to issue a repeat command at a period 1/4 the 
  // repeat interval.
  setInterval(this.repeatCommand, interval/4);
}


//==========================================================================
// KeyControl
// Keeps track of which keys are pressed and sends appropriate commands
// to the robot.
//==========================================================================
function KeyControl(serverLink){
  this.serverLink=serverLink;
  this.pressed=[];
}

KeyControl.prototype.driveCommand = function(){
  // Single key pressed.
  if(this.pressed[LEFT] && !this.pressed[RIGHT] && !this.pressed[UP] && !this.pressed[DOWN])
    this.serverLink.sendCommand("turnLeft", "drive");
  else if(!this.pressed[LEFT] && this.pressed[RIGHT] && !this.pressed[UP] && !this.pressed[DOWN])
    this.serverLink.sendCommand("turnRight", "drive");
  else if(!this.pressed[LEFT] && !this.pressed[RIGHT] && this.pressed[UP] && !this.pressed[DOWN])
    this.serverLink.sendCommand("driveForward", "drive");
  else if(!this.pressed[LEFT] && !this.pressed[RIGHT] && !this.pressed[UP] && this.pressed[DOWN])
    this.serverLink.sendCommand("driveBack", "drive");
  // Legal two keys combinations.
  else if(this.pressed[LEFT] && !this.pressed[RIGHT] && this.pressed[UP] && !this.pressed[DOWN])
    this.serverLink.sendCommand("driveLeft", "drive");
  else if(!this.pressed[LEFT] && this.pressed[RIGHT] && this.pressed[UP] && !this.pressed[DOWN])
    this.serverLink.sendCommand("driveRight", "drive");
  else if(this.pressed[LEFT] && !this.pressed[RIGHT] && !this.pressed[UP] && this.pressed[DOWN])
    this.serverLink.sendCommand("backLeft", "drive");
  else if(!this.pressed[LEFT] && this.pressed[RIGHT] && !this.pressed[UP] && this.pressed[DOWN])
    this.serverLink.sendCommand("backRight", "drive");
  // All other key combinations stop driving.
  else this.serverLink.sendCommand("stopDriving", "");
}

KeyControl.prototype.liftCommand = function(){
  if(this.pressed[PAGEUP] && !this.pressed[PAGEDOWN])
    this.serverLink.sendCommand("liftClaw", "claw");
  else if(!this.pressed[PAGEUP] && this.pressed[PAGEDOWN])
    this.serverLink.sendCommand("lowerClaw", "claw");
  else
    this.serverLink.sendCommand("stopLift", "");
}

KeyControl.prototype.clawCommand = function(){
  if(this.pressed[HOME] && !this.pressed[END])
    this.serverLink.sendCommand("openClaw", "claw");
  else if(!this.pressed[HOME] && this.pressed[END])
    this.serverLink.sendCommand("closeClaw", "claw");
  else
    this.serverLink.sendCommand("stopClaw", "");
}

KeyControl.prototype.reset = function(){
  this.pressed=[];
}

KeyControl.prototype.down = function(event){
  var key=event.keyCode;
  if(!this.pressed[key]){ // Take action only if newly pressed down.
    this.pressed[key]=true;

    if(key==UP || key==DOWN || key==LEFT || key==RIGHT){
      this.driveCommand();
    }else if(key==PAGEUP || key==PAGEDOWN){
      this.liftCommand();
    }else if(key==HOME || key==END){
      this.clawCommand();
    }else if(key==S_KEY){
      this.serverLink.sendCommand("suspend", "");
    }else if(key==ESC){
      this.serverLink.sendCommand("stop", "");
      if(window.confirm("Do you want the robot to shut down?")==true)
        this.serverLink.sendCommand("exit", "");
    }
  }
}

KeyControl.prototype.up = function(event){
  var key=event.keyCode;
  this.pressed[key]=false;

  if(key==UP || key==DOWN || key==LEFT || key==RIGHT)
    this.driveCommand();
  else if(key==PAGEUP || key==PAGEDOWN)
    this.liftCommand();
  else if(key==HOME || key==END)
    this.clawCommand();
}

//================================================================
// Listen for key presses in window.
//================================================================
var serverLink = new ServerLink();
// serverLink.startTimer(REPEAT_CMD_INTERVAL);
var keyControl = new KeyControl(serverLink);
window.onkeydown = function(e) { keyControl.down(e); }
window.onkeyup = function(e) { keyControl.up(e); }
setInterval(callRepeatCommand, REPEAT_CMD_INTERVAL/4);