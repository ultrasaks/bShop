<?php

$search_word=$_GET['word'];
$string = file_get_contents("app_list.json");
$jfo = json_decode($string);

$posts = $jfo;

$count = 1;
$apps = array();
foreach ($posts as $post) {
    $pos = strpos($post->name, $search_word);
    if ( $pos !== false ) {
       array_push($apps, $count);
    }
    $count++;
}
echo json_encode($apps);
?>