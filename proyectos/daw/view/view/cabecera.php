<?php

    session_start();

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <title>Álbumnes de fotos Sunegami</title>
    <meta name="description" content="Crea tus propios albumnes de fotos"/>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="./imagenes/sunegamilogo.png">
    <link rel="stylesheet" href="estilo.css" media="screen" title="Modo principal">

    <!--Letra accesible-->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible&display=swap" rel="stylesheet">
    
    <!-- Modos de la página -->
    <link rel="alternate stylesheet" href="estilo-oscuro.css" title="Modo oscuro">
    <link rel="alternate stylesheet" href="estilo-grande.css" title="Modo grande">
    <link rel="alternate stylesheet" href="estilo-accesible.css" title="Modo accesible">
    <link rel="alternate stylesheet" href="alto-contraste.css" title="Modo alto contraste">
    <link rel="alternate stylesheet" href="estilo-grande+vision.css" title="Modo grande+vision">
    


    <link rel="stylesheet" href ="impresion.css" media="print">
    <link rel="stylesheet" href ="fontello/css/fontello.css">
    
    

    <script src="javas.js"></script>
    <title>Página Inicio-SUNEGAMI</title>
</head>
<body>
    <header>
        <a href="./"><img src="./imagenes/sunegamilogo.png" alt="logo" id="logo"></a>
        <form id="botbus" action="resultado" method="get">
            <button type="submit" class="icon-search" name="consulta">
            </button>
            <input type="search" class="busqueda" name="consulta">  
        </form>
        <aside>
            <ul>
                <li>
                    <button onclick="document.getElementById('login').style.display='block'" class="icon-login">Iniciar</button>
                </li>
                <li>
                    <button onclick="document.getElementById('registro').style.display='block'" class="icon-user-plus">Registro</button>
                </li>
            </ul> 
        </aside> 
        <nav id="menu">
            <label for="chkMenu">&equiv;</label>
            <input type="checkbox" id="chkMenu">
            <ul>
                <li><a href="./" class="icon-home"><span>Inicio</span></a></li>
                <li><a href="buscar" class="icon-search"><span>Buscar</span></a></li>
            </ul>
        </nav>       
    </header>