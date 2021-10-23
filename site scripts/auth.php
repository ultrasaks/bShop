<?php

if ( $_GET["login"] & $_GET["password"] ){
	if ( file_exists("users/" . $_GET["login"] . "/" . $_GET["login"] . ".php") ){
		$spassword = file_get_contents("users/" . $_GET["login"] . "/" . $_GET["login"] . ".php");
		if ( md5($_GET["password"]) == $spassword ){
			echo "Success";
		} else {
			echo "Wrong password";
		}
	} else {
		echo "User not found";
	}
} else {
	echo "DataNotFound";
}

?>