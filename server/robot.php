<?php
if($_SERVER['REQUEST_METHOD']=='POST'){
  if($_POST['request']=='get_users' ||
     $_POST['request']=='start_session' || $_POST['request']=='end_session' ||
     $_POST['request']=='send_command' || $_POST['request']=='get_command'){
    # Since the request is legal, open a connection to database.
    $servername="localhost";
    $username="bicyclet_dbagent";
    $db_password="c2.99792458";
    $db_name="bicyclet_robot";
    $conn=new mysqli($servername, $username, $db_password, $db_name);
    if($conn->connect_error)
      die("Connection failed:  " . $conn->connect_error);

    if($_POST['request']=='get_users'){ 
      # Return a list of all user names that have a matching robot password.
      $robot_password=$_POST['robot_password'];
      if(!preg_match('/^[\w\s]+$/', $robot_password))
	die("Illegal robot password.");
      $sql="select name from robots where robot_password='$robot_password'";
      if(!$result=$conn->query($sql))
        die("Error running query:  " . $conn->error);
      if($result->num_rows==0)
        die("No users found.<br>");
      while($row=$result->fetch_assoc()){
	print($row['name'] . "\n");
      }
    }else{
      # All other requests require a session # and user password.
      $session_string=filter_var($_POST['session'], FILTER_SANITIZE_NUMBER_INT);
      $session=filter_var($session_string, FILTER_VALIDATE_INT);
      $user_pswd_string=filter_var($_POST['user_password'], FILTER_SANITIZE_NUMBER_INT);
      $user_password=filter_var($user_pswd_string, FILTER_VALIDATE_INT);
      if($session==0 || $user_password==0)die("Session and password cannot be 0.");

      if($_POST['request']=='start_session'){
        # Check for matching robot name/password in database.
        $name=$_POST['name'];
        $robot_password=$_POST['robot_password'];
        if(!preg_match('/^[\w\s]+$/', $name))
  	  die("Illegal user name:  $name");
        if(!preg_match('/^[\w\s]+$/', $robot_password))
  	  die("Illegal robot password.");
        $sql="select `session`, `email` from robots where name='$name' and robot_password='$robot_password'";
        if(!$result=$conn->query($sql))
          die("Error running query:  " . $conn->error);
        if($result->num_rows==0)
          die("No matching name+password.<br>");
        if($result->num_rows>1)
          die("Multiple matching names.");
        $row=$result->fetch_assoc();

        # Remove any named pipe that might linger from previous session.
        if($row['session'] != 0)exec("rm -f robot_fifo_" . $row['session']);

        $email=$row['email'];

        # Update row with new session and user_password, and create a new
        # named pipe for communication.
        $sql="update robots set `session`=$session, user_password=$user_password " .
  	     "where name='$name' and robot_password='$robot_password'";
        if(!$result=$conn->query($sql))
          die("Error running query:  " . $conn->error);
        exec("mkfifo robot_fifo_$session");
        print("Started session $session.");
        send_email($name, $email, $session, $user_password);
      }else{
        $sql="select name from robots where `session`=$session and user_password=$user_password";
        if(!$result=$conn->query($sql))
          die("Error running query:  " . $conn->error);
        if($result->num_rows==0)
		die("No matching session+password. REQUEST=" . $_POST['request'] . "<br>");
        if($result->num_rows>1)
          die("Multiple matching sessions.");

        if($_POST['request']=='send_command'){
          $command=filter_var($_POST['command'], FILTER_SANITIZE_STRING,
                              FILTER_FLAG_STRIP_LOW);
          $command=filter_var($command, FILTER_SANITIZE_STRING,
                              FILTER_FLAG_STRIP_HIGH);
          $quantity_string=filter_var($_POST['quantity'], FILTER_SANITIZE_NUMBER_INT);
          $quantity=filter_var($quantity_string, FILTER_VALIDATE_INT);
          if(($fifo=fopen("robot_fifo_$session", "w"))===FALSE)
            die("Could not open robot_fifo_$session.");
  	  $msg="$command $quantity";
	  if((fwrite($fifo, $msg))===FALSE)
	    die("Failed to send message.");
          print("Sent message:  $msg");
        }elseif($_POST['request']=='get_command'){
    	  if(($fifo=fopen("robot_fifo_$session", "r"))===FALSE)
	    die("Could not open robot_fifo_$session.");
	  while(($msg=fgets($fifo))!==FALSE){
	    print("$msg\n");
	  }
        }elseif($_POST['request']=='end_session'){
          # Change session=0 and user_password=0 to show they are invalid,
          # and delete the associated named pipe.
          $sql="update robots set `session`=0, user_password=0 " .
  	       "where session=$session and user_password=$user_password";
          if(!$result=$conn->query($sql))
            die("Error running query:  " . $conn->error);
          exec("rm -f robot_fifo_$session");
        }
      }
    }
  }else{
    print("Bad request.");
  }
}

function send_email($name, $email, $session, $user_password){
	$to = $email;
	$subject = "Robot waiting for commands";
	$headers = "MIME-Version: 1.0\r\n" .
		"Content-type:text/html;charset=UTF-8\r\n" .
		"From:  daniel@bicycletrip.org\r\n";
	$body = "<html>\r\n" .
		"<head><title>Robot waiting for commands</title></head>\r\n" .
		"<body>\r\n" .
		"<p>$name,</p>\r\n" .
		"<p>A robot is ready for you to control it.  Use a web browser\r\n" .
		"to send commands to the robot, and use Skype to see and hear\r\n" .
		"the robot's surroundings.  The following two URLs will open\r\n" .
		"the command web page and start a Skype call:</p>\r\n" .
		"<ul>\r\n" .
		"<li><a href=\"http://www.bicycletrip.org/robot/robot_control.html?" .
		"session=$session&user_password=$user_password\">" .
		"Robot control web page</a></li>\r\n" .
		"<li><a href=\"skype:kathy.mcgrath75\">Call with Skype</a><br>\r\n" .
		"(If \"Call with Skype\" is not a link, then enter this URL in your\r\n" .
	        "browser:  skype:kathy.mcgrath75?call )\r\n" .
		"</li>\r\n" .
		"</ul>\r\n" .
		"</body>\r\n" .
		"</html>\r\n";
	mail($to, $subject, $body, $headers);
}
?>
