<?php


$request_uri = $_SERVER['REQUEST_URI'];

// Dividir la URI en partes
$url_parts = explode('?', $request_uri);

// Tomar la ruta de la URL (parte antes del '?')
$path = $url_parts[0];

switch ($path) {
    case '/daw/':
        include ('view/index.php');
        break;
    case '/daw/accesibilidad':
        include ('view/accesibilidad.php');
        break;
    case '/daw/album':
        include ('view/album.php');
        break;
    case '/daw/albumes':
        include ('view/albumes.php');
        break;
    case '/daw/anyadirFoto':
        include ('view/anyadirFoto.php');
        break;
    case '/daw/buscar':
        include ('view/buscar.php');
        break; 
    case '/daw/configurar':
        include ('view/configurar.php');
        break; 
    case '/daw/crear_album':
        include ('view/crear_album.php');
        break; 
    case '/daw/datos':
        include ('view/datos.php');
        break;
    case '/daw/detalle':
        include ('view/detalle.php');
        break;
    case '/daw/errores':
        include ('view/errores.php');
        break;
    case '/daw/fotos':
        include ('view/fotos.php');
        break;
    case '/daw/inicio.php':
        include ('view/view/inicio.php');
        break; 
    case '/daw/mensaje_error':
        include ('view/mensaje_error.php');
        break;
    case '/daw/perfil':
        include ('view/perfil.php');
        break;
    case '/daw/resultado':
        include ('view/resultado.php');
        break;
    case '/daw/res_album':
        include ('view/res_album.php');
        break;
    case '/daw/res_foto':
        include ('view/res_foto.php');
        break;
    case '/daw/res_registro':
        include ('view/res_registro.php');
        break;
    case '/daw/res_datos':
        include ('view/res_datos.php');
        break;
    case '/daw/respuesta_solicitar_album':
        include ('view/respuesta_solicitar_album.php');
        break;  
    case '/daw/solicitar_album':
        include ('view/solicitar_album.php');
        break; 
    
    default:
        header('HTTP/1.0 404 Not Found');
        echo <<<hereDoc
        <head>
        <link rel="stylesheet" href="estilo.css" media="screen" title="Modo principal">
        </head>
        <aside id=pag_error>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Página no encontrada</p>
        </fieldset>
        </aside>
     
        hereDoc;

        break;
}
?>