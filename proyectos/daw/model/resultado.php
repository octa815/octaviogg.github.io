<?php
$titulo = isset($_GET['titulo']) ? $_GET['titulo'] : '';
$fecha = isset($_GET['fecha']) ? $_GET['fecha'] : '';
$pais = isset($_GET['pais']) ? $_GET['pais'] : '';
$consulta = isset($_GET['consulta']) ? $_GET['consulta'] : '';

$result = mysqli_query($connect,
    "SELECT * FROM fotos as f
    INNER JOIN paises as p ON f.Pais = p.IdPais
    WHERE 
        (LOWER(Titulo) LIKE LOWER('%$consulta%'))
        AND(LOWER(Titulo) LIKE LOWER('%$titulo%')
        AND(LOWER(Pais) LIKE LOWER('%$pais%')
        AND Fecha LIKE '%$fecha%'))"
);
?>