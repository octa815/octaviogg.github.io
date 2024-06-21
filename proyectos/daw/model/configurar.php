<?php
// Verificar si hay una sesión de usuario activa
if(isset($_COOKIE["usuario"])) {
    // Obtener el nombre del usuario actual
    $usuarioActual = $_COOKIE["usuario"];
} else {
    // Manejar el caso en que no haya una sesión de usuario activa
    echo "No hay una sesión de usuario activa.";
}
    
    $result = mysqli_query($connect,
    "SELECT
    IdEstilo,
    Nombre,
    Descripcion,
    Fichero
    FROM estilos"
    );
?>