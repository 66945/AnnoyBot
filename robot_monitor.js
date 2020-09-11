var xhttp=new XMLHttpRequest();
var keep_going=0, user_name=0, robot_password=0, session=0, user_password=0;
var command_display;

function get_users(){
  command_display=document.getElementById("command");
  robot_password=document.getElementById("robot_password").value;
  xhttp.open("POST", "robot.php", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var request_string="request=get_users" +
                     "&robot_password=" + robot_password;
  xhttp.send(request_string);
}

function start(){
  keep_going=1;
  command_display=document.getElementById("command");
  user_name=document.getElementById("user_name").value;
  robot_password=document.getElementById("robot_password").value;
  session=document.getElementById("session").value;
  user_password=document.getElementById("user_password").value;
  xhttp.open("POST", "robot.php", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var request_string="request=start_session" +
                     "&name=" + user_name +
                     "&robot_password=" + robot_password +
                     "&session=" + session +
                     "&user_password=" + user_password;
  xhttp.send(request_string);
}

function stop(){
  keep_going=0;
  xhttp.open("POST", "robot.php", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var request_string="request=end_session" +
                     "&session=" + session +
                     "&user_password=" + user_password;
  xhttp.send(request_string);
}

function getCommand(){
  xhttp.open("POST", "robot.php", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var request_string="request=get_command" +
                     "&session=" + session +
                     "&user_password=" + user_password;
  xhttp.send(request_string);
}

function getResponse(){
  if(xhttp.readyState==4){
    if(xhttp.status==200){
      command_display.innerHTML="<pre>" + xhttp.responseText + "</pre><br>" +
                                xhttp.statusText;
      if(keep_going)getCommand();
    }else if(xhttp.status==405 || xhttp.status==408){
      command_display.innerHTML="Request timeout, issuing new request.";
      if(keep_going)getCommand();
    }else{
      command_display.innerHTML="Bad response: " + xhttp.status;
    }
  }
}

xhttp.onreadystatechange=getResponse;