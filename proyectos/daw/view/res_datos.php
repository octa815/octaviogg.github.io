<?php
if (isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
} else {
    echo "No hay una sesión de usuario activa.";
    exit();
}

include("model/conexion.php");

$usu = mysqli_query($connect, "SELECT * FROM usuarios WHERE NomUsuario ='$usuarioActual'");
$usuario = mysqli_fetch_assoc($usu);

$id_usuario = $usuario['IdUsuario'];
$hoy = date("Y-m-d H:i:s");

// Campos del formulario
$campos = array(
    'NomUsuario' => isset($_GET["nombre_reg"]) ? $_GET["nombre_reg"] : $usuario['NomUsuario'],
    'Clave' => isset($_GET["pass_reg"]) ? $_GET["pass_reg"] : $usuario['Clave'],
    'Email' => isset($_GET["email_reg"]) ? $_GET["email_reg"] : $usuario['Email'],
    'Sexo' => isset($_GET["sexo"]) ? $_GET["sexo"] : 'Prefiero no decirlo',
    'FNacimiento' => isset($_GET["fecha1"]) ? $_GET["fecha1"] : $usuario['FNacimiento'],
    'Ciudad' => isset($_GET["ciudad"]) ? $_GET["ciudad"] : $usuario['Ciudad'],
    'Pais' => isset($_GET["pais"]) ? $_GET["pais"] : $usuario['Pais']
);

// Validaciones y construcción de la consulta
$setClause = "";
$tipos = "";
$valores = array();

foreach ($campos as $campo => $valor) {
    if (!empty($valor)) {

        // Añade el campo a la cláusula SET
        $setClause .= "$campo = ?, ";
        $tipos .= "s";
        $valores[] = $valor;
    }
}

// Elimina la última coma y espacio en blanco de la cláusula SET
$setClause = rtrim($setClause, ', ');

// Construye la consulta
$update = "UPDATE usuarios SET $setClause, FRegistro = ? WHERE IdUsuario = ?";
$tipos .= "si";
$valores[] = $hoy;
$valores[] = $id_usuario;


$stmt = mysqli_prepare($connect, $update);


mysqli_stmt_bind_param($stmt, $tipos, ...$valores);


if (!mysqli_stmt_execute($stmt)) {
    die("Error: no se pudo realizar la actualización");
}

mysqli_stmt_close($stmt);
mysqli_close($connect);

// Actualizar sesiones
$_SESSION["usuario"] = $campos['NomUsuario'];
$_SESSION["psw"] = $campos['Clave'];

// Actualizar cookies
setcookie("usuario", $campos['NomUsuario'], time() + 90 * 24 * 60 * 60);
setcookie("psw", $campos['Clave'], time() + 90 * 24 * 60 * 60);
require_once('view/cabecera_privada.php');
echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset id="succes" >
        <legend>ENHORABUENA!!</legend>
        <p>Usuario actualizado</p>
            <input type="button"  onclick="location.href='./';"value= "OK" />
        </fieldset>    
    </aside>  
</main>
hereDoc;
?>

<?php    
require_once('view/inicio.php');
?>
<?php    
require_once('view/pie.php');
?>