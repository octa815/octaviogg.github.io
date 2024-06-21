<?php
for ($i = 1,$f = 3; $i <= 15; $i++,$f+=3) {
    echo "<tr>";
    echo "<td>$i</td>"; // Número de páginas
    echo "<td>$f</td>"; // Número de fotos

    // Calcula los costos para diferentes configuraciones
    $costoNegro150_300 = calcularCostoAlbum($i, $f, false, 150);
    $costoNegro450_900 = calcularCostoAlbum($i, $f, false, 450);
    $costoColor150_300 = calcularCostoAlbum($i, $f, true, 150);
    $costoColor450_900 = calcularCostoAlbum($i, $f, true, 450);

    echo "<td>" . number_format($costoNegro150_300, 2) . " €</td>";
    echo "<td>" . number_format($costoNegro450_900, 2) . " €</td>";
    echo "<td>" . number_format($costoColor150_300, 2) . " €</td>";
    echo "<td>" . number_format($costoColor450_900, 2) . " €</td>";
    echo "</tr>";
}

function calcularCostoAlbum($numPaginas, $numFotos, $color, $resolucion)
{
    $costo = 0.10 * $numPaginas;

    if ($numPaginas >= 5 && $numPaginas <= 11) {
        $costo = 0.08 * $numPaginas + 0.08;
    } elseif ($numPaginas > 11) {
        $costo = 0.07 * $numPaginas + 0.19;
    }

    if ($color) {
        $costo += 0.05 * $numFotos;
    }

    if ($resolucion > 300) {
        $costo += 0.02 * $numFotos;
    }

    return $costo;
}


?>