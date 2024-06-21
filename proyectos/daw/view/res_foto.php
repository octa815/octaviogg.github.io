<?php
include("view/cabecera_privada.php");
include('model/conexion.php');

// Validar y limpiar datos
$titulo = isset($_POST["titulo"]) ? mysqli_real_escape_string($connect, $_POST["titulo"]) : '';
$descripcion = isset($_POST["descripcion"]) ? mysqli_real_escape_string($connect, $_POST["descripcion"]) : '';
$fecha = isset($_POST["fecha"]) ? mysqli_real_escape_string($connect, $_POST["fecha"]) : '';
$pais = isset($_POST["pais"]) ? mysqli_real_escape_string($connect, $_POST["pais"]) : '';
$album = isset($_POST["album"]) ? mysqli_real_escape_string($connect, $_POST["album"]) : '';
$foto = isset($_POST["foto"]) ? './imagenes/' . mysqli_real_escape_string($connect, $_POST["foto"]) : '';
$alternativo = isset($_POST["alternativo"]) ? mysqli_real_escape_string($connect, $_POST["alternativo"]) : '';
$hoy = date("Y-m-d H:i:s");

// Validar que titulo, album y alternativo no estén en blanco
if (empty($titulo) || empty($album) || empty($alternativo)) {
    echo <<<hereDoc
    <main id="pag_error">
        <fieldset>
            <legend class="error_pag">ADVERTENCIA</legend>
            <p>Error: El título, el álbum y el texto alternativo no pueden estar en blanco.</p>
            <input type="button" onclick="location.href='anyadirFoto';" value="Volver" />
        </fieldset>
    </main>
    hereDoc;
    exit();
}

// Preparar la consulta SQL
$insert = "INSERT INTO fotos (
    titulo, 
    descripcion, 
    fecha, 
    pais, 
    album, 
    fichero, 
    alternativo, 
    FRegistro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
$stmt = mysqli_prepare($connect, $insert);

if ($stmt) {
    mysqli_stmt_bind_param($stmt, "ssssssss", $titulo, $descripcion, $fecha, $pais, $album, $foto, $alternativo, $hoy);

    if (mysqli_stmt_execute($stmt)) {
        echo <<<hereDoc
        <main id="pag_error">
            <aside>
                <fieldset id="succes" >
                    <legend>ENHORABUENA!!</legend>
                    <p>Foto insertada con éxito</p>
                    <ul>
                        <li>Título: $titulo</li>
                        <li>Descripción: $descripcion</li>
                        <li>Fecha: $fecha</li>
                        <li>País: $pais</li>
                        <li>Álbum: $album</li>
                        <li>Fichero: $foto</li>
                        <li>Alternativo: $alternativo</li>
                        <li>Fecha de subida: $hoy</li>
                    </ul>
                    <input type="button" onclick="location.href='./';" value="OK" />
                </fieldset>    
            </aside>  
        </main>
        hereDoc;
    } else {
        die("Error: no se pudo realizar la inserción - " . mysqli_error($connect));
    }

    mysqli_stmt_close($stmt);
} else {
    die("Error: no se pudo preparar la inserción");
}

mysqli_close($connect);

require_once('view/inicio.php');
require_once('view/pie.php');
?>