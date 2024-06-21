<?php
if (isset($_GET["nomUsuario"])) {
    $nomUsuario = $_GET["nomUsuario"];
}
$result = mysqli_query($connect, 
    "SELECT * FROM usuarios
    INNER JOIN paises as p ON Pais = p.IdPais 
    WHERE NomUsuario = $nomUsuario
");

if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
}
    $res = mysqli_query($connect, 
        "SELECT 
        a.IdAlbum,
        a.Titulo,
        a.Descripcion
        FROM albumes as a
        INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
        WHERE u.NomUsuario = '$usuarioActual' " 
    );
?>