<?php
$string = file_get_contents("app_list.json");
$jfo = json_decode($string, true);
echo count($jfo);
?>