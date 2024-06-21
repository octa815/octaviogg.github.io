<?php
// Verificar si hay una sesión de usuario activa
if(isset($_COOKIE["usuario"])) {
    // Obtener el nombre del usuario actual
    $usuarioActual = $_COOKIE["usuario"];
} else {
    // Manejar el caso en que no haya una sesión de usuario activa
    echo "No hay una sesión de usuario activa.";
}
    
   // Realizar la consulta para obtener todas las fotos del usuario
    $result = mysqli_query($connect,
    "SELECT
    u.NomUsuario,
    f.IdFoto,
    f.Titulo,
    f.Descripcion,
    f.Fecha,
    f.Album,
    f.Fichero,
    f.Alternativo,
    p.NomPais,
    a.Titulo as TituloAlbum
    FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE u.NomUsuario = '$usuarioActual'"
    );

?>