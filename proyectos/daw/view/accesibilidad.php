<?php    
    if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])){
    
        include('view/cabecera.php');

    }else{

        include("view/cabecera_privada.php");

    }
?>
<main>

    <h1>Declaración de Accesibilidad</h1>
    <fieldset>
        <legend>SUNEGAMI</legend>
        <p>En Sunegami ®, nos comprometemos a brindar una experiencia en línea accesible y amigable para todos nuestros visitantes. Para lograrlo, hemos implementado diversas prácticas de accesibilidad que se reflejan en los siguientes aspectos:</p>
    </fieldset>
    
    <fieldset>
        <legend>Etiquetado Semántico</legend>
        <p>Esta página web utiliza etiquetas semánticas HTML5 para estructurar el contenido de manera significativa. Se utilizan encabezados, párrafos, listas y otros elementos HTML de acuerdo con su propósito.</p>
        <p>Hemos priorizado el etiquetado semántico en todo nuestro código HTML. Esto significa que utilizamos etiquetas HTML de manera coherente y significativa para describir la estructura y el contenido de nuestras páginas. Esto facilita la navegación y comprensión del contenido, especialmente para usuarios que utilizan lectores de pantalla o tecnologías de asistencia.</p>
    </fieldset>
    
    <fieldset>
        <legend>Texto Alternativo de las Imágenes</legend>
        <p>Todas las imágenes de esta página incluyen atributos "alt/title" descriptivos que proporcionan una alternativa textual para el contenido visual. Esto ayuda a usuarios con discapacidades visuales a comprender el contenido de las imágenes.</p>
    </fieldset>
    
    <fieldset>
        <legend>Uso de Colores Accesibles</legend>
        <p>Los colores utilizados en esta página se han seleccionado cuidadosamente para garantizar un alto contraste y legibilidad mediante<a href=" https://webaim.org/resources/contrastchecker/" data-link=" https://webaim.org/resources/contrastchecker/"> WebAim</a>. Se evitan combinaciones de colores que puedan dificultar la lectura o causar problemas de accesibilidad.</p>
        <p>También evitamos utilizar únicamente el color como medio para transmitir información importante, asegurándonos de que existan indicadores adicionales, como etiquetas o íconos, para comunicar contenido relevante.</p>
    </fieldset>
    
    <fieldset>
        <legend>Hoja de Estilo Accesible</legend>
        <p>Nuestra hoja de estilo CSS se ha desarrollado teniendo en cuenta la accesibilidad. Hemos evitado el uso de estilos que puedan dificultar la lectura o la navegación para personas con discapacidades. Además, hemos proporcionado opciones de aumento y disminución del tamaño del texto para brindar una experiencia más personalizada.</p>
    </fieldset>
    
    
    <br>
    <hr>
    <fieldset>
        <p>Estamos comprometidos a seguir mejorando nuestra accesibilidad web y a garantizar que todas las personas puedan disfrutar plenamente de nuestro contenido. Si tienes alguna sugerencia o encuentras algún problema relacionado con la accesibilidad en nuestro sitio web, no dudes en contactarnos. Tu retroalimentación es invaluable para nosotros.</p>
        <p>Gracias por visitar Sunegami ® y por apoyar nuestro compromiso con la accesibilidad web.</p>
    </fieldset>
    
</main>
  
<!--************************************************************************************-->
<?php    
    require_once('view/inicio.php');
?>
<!--************************************************************************************-->
<?php    
  require_once('view/pie.php');
?>