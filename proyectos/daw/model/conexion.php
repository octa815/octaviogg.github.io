<?php
    $connect = @mysqli_connect(
    "localhost",
    "root",
    "",
    "sunegami");
    if(!$connect){
     echo '<p>Error al conectar con la base de datos: ' . mysqli_connect_error();
    exit;
}
?>
