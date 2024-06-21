<?php
if (!isset($_COOKIE["usuario"])) {
    echo "No hay una sesión de usuario activa.";
    exit();
}

$usuarioActual = $_COOKIE["usuario"];
require_once('view/cabecera_privada.php');
include("model/conexion.php");

$titulo = isset($_POST["titulo"]) ? mysqli_real_escape_string($connect, $_POST["titulo"]) : null;
$descripcion = isset($_POST["desc"]) ? mysqli_real_escape_string($connect, $_POST["desc"]) : null;

if (empty($titulo)) { 
    echo <<<hereDoc
    <main id=pag_error>
    <fieldset>
    <legend class="error_pag">WARNING!!</legend>
        <p>Error: El título es obligatorio. Por favor, proporciona un título.</p>
    </fieldset>
    </main>
hereDoc;
    exit(); 
}

$usu = mysqli_query($connect, "SELECT * FROM usuarios WHERE NomUsuario ='$usuarioActual'");
$user = mysqli_fetch_assoc($usu);
$usuario = $user['IdUsuario'];

$insert = "INSERT INTO albumes (
    titulo, 
    descripcion, 
    Usuario
    ) VALUES (?, ?, ?)";
$stmt = mysqli_prepare($connect, $insert);

mysqli_stmt_bind_param($stmt, "ssi", $titulo, $descripcion, $usuario);

if (!mysqli_stmt_execute($stmt)) {
    die("Error: no se pudo realizar la inserción - " . mysqli_error($connect));
}

mysqli_stmt_close($stmt);
mysqli_close($connect);

echo <<<hereDoc
<main id="pag_error">
    <aside>
        <fieldset id="succes" >
            <legend>ENHORABUENA!!</legend>
            <p>Álbum creado con éxito, </p>
            <p>!! Añade tu primera foto ¡¡</p>
            <input type="button" onclick="location.href='anyadirFoto';" value="OK" />
        </fieldset>    
    </aside>  
</main>
hereDoc;

require_once('view/inicio.php');
require_once('view/pie.php');
?>