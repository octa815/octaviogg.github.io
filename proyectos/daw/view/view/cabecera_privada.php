<?php
    include('model/conexion.php');
    include('./controller/sesion.php');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Álbumnes de fotos Sunegami</title>
    <meta name="description" content="Crea tus propios albumnes de fotos"/>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="./imagenes/sunegamilogo.png">

    <?php
        // Obtener el estilo del usuario desde la cookie
        $estiloCookie = isset($_COOKIE['estilo']) ? $_COOKIE['estilo'] : '';

        // Si no hay estilo en la cookie, intentar obtenerlo de la base de datos
        if (empty($estiloCookie) && isset($_COOKIE['usuario'])) {
            $usuario = $_COOKIE['usuario'];
            $query = "SELECT Estilo FROM usuarios WHERE NomUsuario = '$usuario'";
            $result = mysqli_query($connect, $query);

            if ($result && $row = mysqli_fetch_assoc($result)) {
                $estiloCookie = $row['Estilo'];
            }
        }

        // Obtener el nombre del archivo de estilo correspondiente al ID del estilo
        if (!empty($estiloCookie)) {
            $queryEstilo = "SELECT Fichero FROM estilos WHERE IdEstilo = $estiloCookie";
            $resultEstilo = mysqli_query($connect, $queryEstilo);

            if ($resultEstilo && $rowEstilo = mysqli_fetch_assoc($resultEstilo)) {
                $ficheroEstilo = $rowEstilo['Fichero'];
                //echo $ficheroEstilo;
                echo '<link rel="stylesheet" href="' . $ficheroEstilo . '"media="screen" title="Modo principal">';
                // Script de JavaScript para recargar la página después de cambiar el estilo
            } else {
                // Manejar el caso en que no se pueda obtener el nombre del estilo
                echo '<!-- Error al obtener el nombre del estilo -->';
            }
        } else {
            // Establecer el estilo predeterminado si no hay estilo en la cookie ni en la base de datos
            echo '<link rel="stylesheet" href="estilo.css"media="screen" title="Modo principal">';
        }
    ?>
    
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
<?php
    include('./model/index.php');
    if (isset($_GET['confirmarBorrado'])) {
        // Verifica si el usuario está autenticado
        if (isset($_COOKIE['usuario'])) {
            // Obtiene el ID del usuario a eliminar
            $usuario_a_eliminar = $_COOKIE['usuario'];
    
            // Obtiene la información de los álbumes y el número total de fotos
            $queryResumen = "SELECT a.Titulo AS NombreAlbum, COUNT(f.IdFoto) AS NumFotosAlbum
                             FROM albumes a
                             LEFT JOIN fotos f ON a.IdAlbum = f.Album
                             WHERE a.Usuario IN (SELECT IdUsuario FROM usuarios WHERE NomUsuario = '$usuario_a_eliminar')
                             GROUP BY a.IdAlbum";
            $resultResumen = mysqli_query($connect, $queryResumen);
    
            if (!$resultResumen) {
                die("Error al obtener el resumen de álbumes: " . mysqli_error($connect));
            }
    
            // Muestra el formulario de confirmación con el resumen de álbumes
            echo <<<HTML
            <main id="pag_confirmacion">
                <aside>
                    <fieldset>
                        <legend>Confirmación de Borrado</legend>
                        <p>¿Estás seguro de que deseas darte de baja? Se eliminarán todos tus datos.</p>
                        
                        <div>
                            <h3>Resumen de álbumes:</h3>
                            <ul>
    HTML;
    
            while ($rowResumen = mysqli_fetch_assoc($resultResumen)) {
                echo "<li>{$rowResumen['NombreAlbum']} - {$rowResumen['NumFotosAlbum']} fotos</li>";
            }
    
            echo <<<HTML
                            </ul>
                        </div>
                        
                        <form method="post" action="?borrar">
                            <label for="password">Introduce tu contraseña:</label>
                            <input type="password" name="password" required>
                            <input type="submit" value="Sí, estoy seguro">
                            <a href="./">Cancelar</a>
                        </form>
                    </fieldset>
                </aside>
            </main>
        HTML;
            exit(); // Evita que el resto del código se ejecute
        }
    }
?>
    <script src="javas.js"></script>
    <title>Página Inicio-SUNEGAMI</title>
</head>
<body>
    <header>
        <a href="./"><img src="./imagenes/sunegamilogo.png" alt="logo"></a>
        <form id="botbus" action="resultado" method="get">
            <button type="submit" class="icon-search" >
            </button>
            <input type="search" class="busqueda" name="consulta">  
        </form>
        <aside>
        <?php
        include('./model/usuario.php');
        if($row = mysqli_fetch_assoc($usua)){
        echo <<<hereDOC
            <figure>
                <button class="mipanel" onclick=openNav()><img src="{$row['Foto']}" alt="user" id="user"></button>
            </figure> 
            <aside id="panel" class="lateral">
                <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">×</a>
                <figure>
                    <img src="{$row['Foto']}" alt="usu" id="usuario">
hereDOC;
}
?>
                    <figcaption class="icon-user-circle-o">Usuario: <?=$_COOKIE["usuario"];?></figcaption>
                
<!--************************************************************************************-->                 
<?php
    if (isset($_SESSION['primer_acceso'])) {
        echo <<<hereDOC
            <li><p>$mensaje</p></li>
        hereDOC;
    }
    echo "<p>$saludo $usu</p>"

?>
<!--************************************************************************************-->
                </figure>

        <a href="datos?nomUsuario='<?=$_COOKIE['usuario'];?>'" class="icon-doc-text">Mis datos</a>

        <a href="albumes" class="icon-folder-open-empty-1">Mis álbumes</a>
        <a href="crear_album" class="icon-folder-add">Crear álbum</a>
        <a href="anyadirFoto" class="icon-picture">Añadir foto</a>
        <a href="solicitar_album" class="icon-edit">Solicitar álbum</a>
        <a href="configurar" class="icon-feather">Configurar</a>
        <a href="?confirmarBorrado" class="icon-trash-empty">Darme de baja</a>
        <!--<a href="#" class="icon-trash-empty" onclick="confirmarBorrado()">Darme de baja</a>-->
        <a href="?logout" class="icon-logout">Cerrar sesión</a>
        
        <script>
            function confirmarBorrado() {
                // Muestra un cuadro de diálogo para confirmar el borrado
                var confirmacion = confirm("¿Estás seguro de que deseas darte de baja? Se eliminarán todos tus datos.");

                // Si el usuario confirma, redirige a la página de borrado
                if (confirmacion) {
                    window.location.href = "?borrar";
                }
            }
        </script>

<?php


if (isset($_GET['borrar'])) {
    // Verifica si el usuario está autenticado
    if (isset($_COOKIE['usuario'])) {
        // Obtiene el ID del usuario a eliminar
        $usuario_a_eliminar = $_COOKIE['usuario'];

        // Elimina los registros relacionados en la tabla fotos
        $borrar_fotos = mysqli_query($connect, "DELETE FROM fotos WHERE Album IN (SELECT IdAlbum FROM albumes WHERE Usuario IN (SELECT IdUsuario FROM usuarios WHERE NomUsuario = '$usuario_a_eliminar'))");

        if (!$borrar_fotos) {
            die("Error al ejecutar la consulta para borrar fotos: " . mysqli_error($connect));
        }

        // Elimina los registros relacionados en la tabla solicitudes
        $borrar_solicitudes = mysqli_query($connect, "DELETE FROM solicitudes WHERE Album IN (SELECT IdAlbum FROM albumes WHERE Usuario IN (SELECT IdUsuario FROM usuarios WHERE NomUsuario = '$usuario_a_eliminar'))");

        // Elimina los registros relacionados en la tabla albumes
        $borrar_albumes = mysqli_query($connect, "DELETE FROM albumes WHERE Usuario IN (SELECT IdUsuario FROM usuarios WHERE NomUsuario = '$usuario_a_eliminar')");

        if (!$borrar_albumes) {
            die("Error al ejecutar la consulta para borrar albumes: " . mysqli_error($connect));
        }

        // Elimina al usuario de la tabla usuarios
        $borrar_usuario = mysqli_query($connect, "DELETE FROM usuarios WHERE NomUsuario = '$usuario_a_eliminar'");
        
        if (!$borrar_usuario) {
            die("Error al ejecutar la consulta para borrar el usuario: " . mysqli_error($connect));
        }

        // Cierra la sesión después de eliminar el usuario
        session_destroy();
        setcookie("usuario", "", time() - 3600);
        setcookie("psw", "", time() - 3600);
        setcookie("ultima_visita", "", time() - 3600);
        setcookie("estilo", "", time() - 3600);

        // Redirige a una página de confirmación o a donde desees
        header('Location: ./');
        exit();
    }
}
?>


<?php
    // Verificar si se ha hecho clic en el enlace de cerrar sesión
    if (isset($_GET['logout'])) {
        session_destroy();
        // Eliminar las cookies
        setcookie("usuario", "", time() - 3600);
        setcookie("psw", "", time() - 3600);
        setcookie("ultima_visita", "", time() - 3600);
        setcookie("estilo", "", time() - 3600);


        // Redirigir a la página de inicio o a donde desees después de cerrar sesión
        header('Location: ./');
        exit();
    }
?>
        <aside class="botoncillo">
            <a class="icon-moon">Claro/oscuro</a>
                <aside class="darkbot">
                <label class="switch">
                    <input type="checkbox" onclick="oscuro()">
                    <span class="slider round"></span>
                </label> 
            </aside> 
        </aside>
        <aside class="botoncillo">
            <a class="icon-fontsize">Tamaño</a>
            <aside class="darkbot">
                <label class="switch">
                    <input type="checkbox" onclick="grande()">
                    <span class="slider round"></span>
                </label> 
            </aside> 
        </aside>
    </aside>             
</aside> 
<nav id="menu"> 
    <label for="chkMenu">&equiv;</label>
    <input type="checkbox" id="chkMenu">
    <ul>
        <li><a href="./" class="icon-home"><span>Inicio</span></a></li>
        <li><a href="buscar" class="icon-search"><span>Buscar</span></a></li>
        <li><a href="solicitar_album" class="icon-doc-add"><span>Solictar álbum</span></a></li>
        <li><a href="?logout" class="icon-logout"><span>Cerrar sesión</span></a></li>
<!--************************************************************************************-->
<?php
    if (!isset($_SESSION['primer'])) {
        echo <<<hereDOC
        <li><p>$mensaje</p></li>
        hereDOC;
        $_SESSION['primer'] = false;
    }
?>  
<!--************************************************************************************-->
        </ul>   
    </nav>   
</header>