<?php
 if (isset($_GET['idFoto'])) {
    $idFoto = $_GET['idFoto'];
 }
 
$result = mysqli_query($connect, 
    "SELECT 
    f.Titulo as titulofoto, 
    f.Descripcion, 
    f.Pais,
    NomPais,
    IdUsuario,
    IdAlbum,
    a.Titulo as tituloalbum,
    NomUsuario,
    Album, 
    Fichero, 
    Alternativo, 
    DATE_FORMAT(Fecha,'%e/%c/%Y')as Fecha  
    FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE IdFoto = $idFoto 
    ");
    $detalle = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $detalle[] = $row;
    } 
    
?>