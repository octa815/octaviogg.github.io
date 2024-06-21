<?php
// Define una variable para el resultado del cálculo
$costoTotal = 0;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Recibe los datos del formulario
    $numCopias = isset($_POST["copias"]) ? (int)$_POST["copias"] : 0;
    $impresionColor = isset($_POST["impresion"]) ? true : false;
    $resolucion = isset($_POST["res"]) ? (float)$_POST["res"] : 0;
    $numFotos = isset($_POST["numFotos"]) ? (float)$_POST["numFotos"] : 0;

    // Realiza cálculos basados en los valores del formulario
    if ($numCopias > 0 && $numCopias < 5) {
        $costoTotal += $numCopias * 0.10;
    } elseif ($numCopias > 4 && $numCopias < 11) {
        $costoTotal += $numCopias * 0.08 + 0.08;
    } elseif ($numCopias >= 11) {
        $costoTotal += $numCopias * 0.07 + 0.19;
    }
    if ($impresionColor) {
        $costoTotal += $numFotos * 0.05;
    }
    if ($resolucion > 300) {
        $costoTotal += $numFotos * 0.02;
    }
}
?>
