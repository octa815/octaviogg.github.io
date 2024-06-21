<?php
// Verificar si hay una sesión de usuario activa
if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
} else {
    echo "No hay una sesión de usuario activa.";
}

    $result = mysqli_query($connect, 
        "SELECT 
        a.IdAlbum,
        a.Titulo,
        a.Descripcion
        FROM albumes as a
        INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
        WHERE u.NomUsuario = '$usuarioActual'"
    );
?>