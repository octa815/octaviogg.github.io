<?php

    if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])){
        include('view/cabecera.php');
    }else{
        include("view/cabecera_privada.php");
    }   
?>
<?php
    require_once("controller/error.php");
?>
<?php    
    require_once('view/inicio.php');
?>
<?php    
    require_once('view/pie.php');
?>