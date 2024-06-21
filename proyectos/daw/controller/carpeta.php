<?php 
$ancho = 300;
$alto = 200;
$image = imagecreatetruecolor($ancho, $alto);

// Definir colores
$fondo_superior = imagecolorallocate($image, 240, 240, 240); // Gris claro (parte superior)
$fondo_inferior = imagecolorallocate($image, 220, 220, 220); // Gris oscuro (parte inferior)
$bordes = imagecolorallocate($image, 0, 0, 0); // Negro

// Rellenar el fondo superior de gris claro
imagefilledrectangle($image, 0, 0, $ancho, $alto / 2, $fondo_superior);

// Rellenar el fondo inferior de gris oscuro
imagefilledrectangle($image, 0, $alto / 2, $ancho, $alto, $fondo_inferior);

// Dibujar los bordes
imagerectangle($image, 0, 0, $ancho - 1, $alto - 1, $bordes);

// Simular las líneas de la carpeta semiabierta hacia arriba
$linea_color = imagecolorallocate($image, 150, 150, 150); // Gris para las líneas

for ($i = 0; $i < 5; $i++) {
    imageline($image, 10 + $i, $alto / 2, 10 + $i, $alto - 10, $linea_color);
}

// Agregar imágenes de fotos simuladas


// Establecer el tipo de contenido a imagen/png
header('Content-type: image/png');

// Mostrar la imagen
imagepng($image);

// Liberar recursos
imagedestroy($image);
imagedestroy($foto1);
imagedestroy($foto2);
?>
    