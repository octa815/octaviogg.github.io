<?php
require_once("view/cabecera_privada.php");
include("model/conexion.php");


if (empty($_POST['album'])) {
    echo <<<hereDoc
    <main id="pag_error">
        <fieldset>
            <legend class="error_pag">ADVERTENCIA</legend>
            <p>Error: El campo 'Álbum de SUNEGAMI' no puede estar vacío.</p>
            <input type="button" onclick="location.href='solicitar_album';" value="Volver" />
        </fieldset>
    </main>
    hereDoc;
    exit();
}
?>

<main>
    <section id="seccion">
        <h2>Resultado de solicitud de impresión de álbum</h2>
    </section>

    <div>
        <fieldset>
            <legend>Confirmación de Solicitud</legend>
            <p>Gracias por solicitar un álbum. A continuación, se muestran los datos que has proporcionado:</p>
            <p>Nombre: <strong><?php echo $_POST['nombre']; ?></strong></p>
            <p>Título del álbum: <strong><?php echo $_POST['titulo']; ?></strong></p>
            <p>Texto adicional: <strong><?php echo $_POST['texto_ad']; ?></strong></p>
            <p>Correo electrónico: <strong><?php echo $_POST['correo']; ?></strong></p>
            <p>Dirección: <strong><?php echo $_POST['direccion']; ?></strong></p>
            <p>Número: <strong><?php echo $_POST['numero']; ?></strong></p>
            <p>CP: <strong><?php echo $_POST['cp']; ?></strong></p>
            <p>Localidad: <strong><?php echo $_POST['ciudad']; ?></strong></p>
            <p>Provincia: <strong><?php echo $_POST['provincia']; ?></strong></p>
            <p>Teléfono: <strong><?php echo $_POST['telefono']; ?></strong></p>
            <p>Color de portada: <input type="color" id="color_portada" name="color_portada" value="#000000" disabled></p>
            <p>Número de copias: <strong><?php echo $_POST['copias']; ?></strong></p>
            <p>Número de fotos: <strong><?php echo $_POST['numFotos']; ?></strong></p>
            <p>Resolución de impresión: <strong><?php echo $_POST['res']; ?></strong></p>
            <p>Álbum de SUNEGAMI: <strong><?php echo $_POST['album']; ?></strong></p>
            <p>Fecha de recepción: <strong><?php echo $_POST['fecha1']; ?></strong></p>
            <p>Impresión a color: <strong><?php echo isset($_POST['impresion']) ? 'Sí' : 'No'; ?></strong></p>
            <?php
            require_once("controller/clc_album.php");
            ?>
            <p id="Coste"><strong>Coste del álbum: <?php echo number_format($costoTotal, 2); ?> €</strong></p>
            <p id="infoResultado">Recibirás un correo electrónico de confirmación con más detalles. Gracias por elegir nuestros servicios.</p>
        </fieldset>
    </div>
</main>

<?php
$insert = "INSERT INTO solicitudes (
    Album, 
    Nombre, 
    Titulo, 
    Descripcion, 
    Email, 
    Direccion, 
    Color, 
    Copias, 
    Resolucion, 
    Fecha, 
    Icolor, 
    FRegistro, 
    Coste
    ) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
$stmt = mysqli_prepare($connect, $insert);

// Verifica si la preparación de la sentencia fue exitosa
if ($stmt) {
$album = $_POST['album'];
$nombre = $_POST['nombre'];
$titulo = $_POST['titulo'];
$texto_ad = $_POST['texto_ad'];
$correo = $_POST['correo'];
$direccion = $_POST['direccion'];
$color_portada = $_POST['color_portada'];
$copias = $_POST['copias'];
$res = $_POST['res'];
$fecha1 = $_POST['fecha1'];
$hoy = date("Y-m-d H:i:s"); 
$impresion = isset($_POST['impresion']) ? 1 : 0; // 1 para Sí, 0 para No

mysqli_stmt_bind_param($stmt, "issssssiisssd",
    $album, 
    $nombre, 
    $titulo, 
    $texto_ad, 
    $correo, 
    $direccion, 
    $color_portada, 
    $copias, 
    $res, 
    $fecha1, 
    $impresion,
    $hoy,
    $costoTotal
);
// Ejecuta la sentencia
if (!mysqli_stmt_execute($stmt)) {
die("Error: no se pudo realizar la inserción");
}

// Cierra la sentencia
mysqli_stmt_close($stmt);
} else {
die("Error: no se pudo preparar la inserción");
}

// Cierra la conexión a la base de datos
mysqli_close($connect);

require_once('view/pie.php');
?>