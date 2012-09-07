<?php 

include 'xmlpostparser.php';

// Parse xml blog post
$posts = XMLPosts($post_path);

foreach($posts as $post){
    echo "<div class=\"" . $post.type . "\">\n";
    foreach($post as $attr){
        echo "<div class=\"" . $attr.type . "\">\n";
        echo $attr.content;
        echo "</div>";
    }
    echo "</div>";
}

?>




