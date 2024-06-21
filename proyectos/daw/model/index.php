<?php
if (isset($_GET['idFoto'])) {
    $idFoto = $_GET['idFoto'];
}

// Realizar la consulta para obtener las 5 últimas fotos
$result = mysqli_query($connect, 
    "SELECT 
    f.Titulo, 
    f.Descripcion, 
    f.Pais,
    NomPais,
    IdUsuario,
    Foto,
    IdFoto,
    NomUsuario,
    Album, 
    Fichero, 
    Alternativo, 
    DATE_FORMAT(f.FRegistro,'%e/%c/%Y') as Fecha  
    FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais 
    INNER JOIN albumes as a ON f.Album = a.IdAlbum
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    ORDER BY f.FRegistro DESC
    LIMIT 5"

);

$principal = mysqli_query($connect,
"SELECT * FROM fotos"
);
?>

