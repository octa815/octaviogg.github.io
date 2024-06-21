<?php
if (isset($_GET['idUsuario'])) {
    $idUsuario = $_GET['idUsuario'];
}
$result = mysqli_query($connect, 
    "SELECT * FROM usuarios as u
    LEFT JOIN albumes as a ON u.IdUsuario = a.Usuario
    WHERE IdUsuario = $idUsuario
    ");
?>