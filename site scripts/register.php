<?php

if ( $_GET["login"] & $_GET["password"] ){
	if ( !file_exists("users/" . $_GET["login"] . "/" . $_GET["login"] . ".php") ){
		mkdir("users/" . $_GET["login"]);
		file_put_contents("users/" . $_GET["login"] . "/" . $_GET["login"] . ".php", md5($_GET["password"]));
		echo "Success";
	} else {
		echo "User already exsists";
	}
} else {
	echo "DataNotFound";
}

?>