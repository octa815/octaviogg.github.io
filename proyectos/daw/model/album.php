<?php
 if (isset($_GET['idAlbum'])) {
    $idAlbum = $_GET['idAlbum'];
 }

 if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
}

    $alb = mysqli_query($connect, 
        "SELECT 
        a.IdAlbum,
        a.Titulo,
        a.Descripcion
        FROM albumes as a
        INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
        WHERE u.NomUsuario = '$usuarioActual'"
    );
 
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
    f.FRegistro,
    DATE_FORMAT(f.FRegistro,'%e/%c/%Y')as Fecha
    FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE idAlbum = $idAlbum 
    "); 
    $albumes = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $albumes[] = $row;
    }

$info = mysqli_query($connect, 
    "SELECT 
    COUNT(f.IdFoto) as numfoto,
    a.Titulo as tituloalbum,
    a.Descripcion as descalbum,
    a.IdAlbum as idAlbum,
    u.NomUsuario,
    GROUP_CONCAT(DISTINCT p.NomPais ORDER BY p.NomPais SEPARATOR ', ') as paises,
    DATE_FORMAT(MIN(f.FRegistro),'%e/%c/%Y')as fecha_antigua,
    DATE_FORMAT(MAX(f.FRegistro),'%e/%c/%Y')as fecha_reciente
    FROM fotos as f
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    WHERE a.IdAlbum = $idAlbum
    GROUP BY a.Titulo, a.Descripcion, u.NomUsuario 
    "); 

    $informacion = array();
    while ($fila = mysqli_fetch_assoc($info)) {
        $informacion[] = $fila;
}
    
?>