<?php
if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
} else {
    echo "No hay una sesión de usuario activa.";
}
$usua = mysqli_query($connect,
"SELECT
NomUsuario,
Foto
FROM usuarios
WHERE NomUsuario = '$usuarioActual'"
);
?>