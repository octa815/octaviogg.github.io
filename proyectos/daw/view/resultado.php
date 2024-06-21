<?php
    if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])){
        include('view/cabecera.php');
    }else{
        include("view/cabecera_privada.php");
    }
include('model/conexion.php');
include('model/resultado.php');
?>
<main>
    <section id="resultados-busqueda">
        <fieldset>
            <h2 class="icon-edit">Resultados de la búsqueda</h2>  
        </fieldset>
        <aside>
        <?php

    if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])) {
        if ($result->num_rows > 0) {
            while ($row = mysqli_fetch_assoc($result)) {
                echo <<<hereDOC
                <figure>
                    <a href="mensaje_error"><img src="{$row["Fichero"]}" alt="imagen"></a>
                    <footer>
                        <fieldset>
                            <legend>{$row["Titulo"]}</legend>
                            <p class="icon-globe">{$row["NomPais"]}</p>
                            <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                            <a href="mensaje_error" id="btnResultado1">Ver detalle</a>
                        </fieldset> 
                    </footer>
                </figure>
                hereDOC;
            }
        } else {
            echo <<<hereDOC
            <fieldset>
                <p>No se encontraron resultados</p>;
            </fieldset> 
            hereDOC;
        }
    } else {
        if ($result->num_rows > 0) {
            while ($row = mysqli_fetch_assoc($result)) {
                echo <<<hereDOC
                <figure>
                    <a href="detalle?idFoto={$row['IdFoto']}"><img src="{$row["Fichero"]}" alt="imagen"></a>
                    <footer>
                        <fieldset>
                            <legend class="icon-picture">{$row["Titulo"]}</legend>
                            <p class="icon-globe">{$row["NomPais"]}</p>
                            <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                            <a href="detalle?idFoto={$row['IdFoto']}" id="btnResultado1" class="icon-eye">Ver detalle</a>
                        </fieldset> 
                    </footer>
                </figure>
                hereDOC;
            }
        } else {
            echo <<<hereDOC
            <fieldset >
                <legend class="error_pag">PELIGRO!!</legend>
                <p>No se encontraron resultados</p>
            </fieldset>
            hereDOC;
        }
    }

?>
        </aside>     
    </section>
</main>
<!--************************************************************************************-->
<?php    
    require_once('view/inicio.php');
?>
<!--************************************************************************************-->
<?php    
    require_once('view/pie.php');
?>