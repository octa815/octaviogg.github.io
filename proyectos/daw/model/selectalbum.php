<?php
if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
} else {
    echo "No hay una sesión de usuario activa.";
}
if (isset($_GET['idAlbum'])) {
    $idAlbum = $_GET['idAlbum'];


    $query = "SELECT 
    IdAlbum, 
    Titulo 
    FROM 
    albumes as a
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE u.NomUsuario = '$usuarioActual' AND IdAlbum != '$idAlbum'
    ";



    $query2 = "SELECT *
    FROM albumes
    WHERE IdAlbum = '$idAlbum'
    ";

    $result2 = $connect->query($query2);
    while ($fila = $result2->fetch_assoc()) {
    echo "<option value='" . $fila['IdAlbum'] . "'>" . $fila['Titulo'] . "</option>";
    }


    $result = $connect->query($query);
    while ($row = $result->fetch_assoc()) {
    echo "<option value='" . $row['IdAlbum'] . "'>" . $row['Titulo'] . "</option>";
    }

}else{
    $query = "SELECT 
    IdAlbum, 
    Titulo 
    FROM 
    albumes as a
    INNER JOIN usuarios as u ON a.Usuario = u.IdUsuario 
    WHERE u.NomUsuario = '$usuarioActual'
    ";
    $result = $connect->query($query);
    echo "<option></option>";
    while ($row = $result->fetch_assoc()) {
    echo "<option value='" . $row['IdAlbum'] . "'>" . $row['Titulo'] . "</option>";
    }
}

?>