<?php

$search_word=$_GET['word'];
$string = file_get_contents("app_list.json");
$jfo = json_decode($string);

$posts = $jfo;

$count = 1;
$apps = array();
foreach ($posts as $post) {
    //echo $post->name;
    //echo '<br>';

    $pos = strpos($post->name, $search_word);

    if ( $pos !== false ) {
       //echo "<b>found $count</b>";
       array_push($apps, $count);
    }
    $count++;

}
echo json_encode($apps);
?>