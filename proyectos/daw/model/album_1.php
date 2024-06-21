<?php
 if (isset($_GET['idAlbum'])) {
    $idAlbum = $_GET['idAlbum'];
 }
 
$result = mysqli_query($connect, 
    "SELECT 
    f.Titulo as titulofoto, 
    f.Descripcion, 
    f.Pais,
    IdFoto,
    NomPais,
    IdUsuario,
    a.Titulo as tituloalbum,
    NomUsuario,
    Album, 
    Fichero, 
    a.Descripcion as descalbum,
    Alternativo, 
    Fecha,
    DATE_FORMAT(Fecha,'%e/%c/%Y')as Fecha
    FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE idAlbum = $idAlbum 
    "); 
?>