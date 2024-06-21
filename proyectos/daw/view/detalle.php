<?php    
    include('view/cabecera_privada.php');
    include('model/conexion.php');
    include('model/detalle.php');
?>

<main>
    <section id="detalle-foto">
        <fieldset id="cabecera">
            <h2 class="icon-eye">Detalle de la Foto</h2>
        </fieldset>
        <?php
       foreach($detalle as $row){
            echo <<<hereDOC
            <figure>
                <img src="{$row["Fichero"]}" alt="Foto Seleccionada">
            </figure>
                <fieldset>
                <legend class="icon-picture">{$row["titulofoto"]}</legend>
                <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                <p class="icon-globe">País: {$row["NomPais"]}</p>
                <a href="perfil?idUsuario={$row['IdUsuario']}">
                <p class="icon-user-circle-o">Usuario: {$row["NomUsuario"]}</p>
                </a>
                <a href="album?idAlbum={$row['IdAlbum']}">
                <p class="icon-folder-open-empty-1">{$row["tituloalbum"]}</p>
                </fieldset>
hereDOC;
}     
        ?>
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