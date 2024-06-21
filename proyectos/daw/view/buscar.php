<?php    
    if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])){
        include('view/cabecera.php');
    }else{
        include("view/cabecera_privada.php");
    }
?>
<?php
    include('model/conexion.php');
?>
<main id="formulario-busqueda">
    <fieldset>
        <legend class="icon-search">Búsqueda de fotos</legend>
        <form action="resultado" method="GET">
            <p>
                <label for="titulo" class="icon-feather">Título:</label>
                <input type="text" id="titulo" name="titulo">
            </p>
            <p>
                <label for="fecha1" class="icon-calendar">Fecha:</label>
                <input type="date" id="fecha" name="fecha">
               
            </p>
            <p>
                <label for="pais" class="icon-globe">País:</label>
                <select type="text" id="pais" name="pais">
                <?php 
                    include('model/pais.php');
                ?>
                </select>
            </p>
            <aside id="boton">
                <button type="submit">Buscar</button>
            </aside>
        </form>
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
