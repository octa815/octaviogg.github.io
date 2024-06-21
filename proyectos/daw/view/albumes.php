
<?php
    if (!isset($_COOKIE["usuario"])) {
        include('view/cabecera.php');
    } else {
        include("view/cabecera_privada.php");
    }

    include('model/conexion.php');
    include('model/albumes.php');
?>

<main>
    <section id="secundaria">
        <fieldset>
            <h2 class="icon-folder-open-empty-1"> TUS ÁLBUMES </h2>
        </fieldset>
        <fieldset>
            <p><a href="fotos" class="icon-picture">Mis fotos </a></p>
        </fieldset> 
        <aside>
            <?php

                while ($row = mysqli_fetch_assoc($result)) {
                    $idAlbum = $row["IdAlbum"];
                    echo <<<hereDOC
                    <figure>
                        <footer>
                            <fieldset>
                                <legend class="icon-folder-open-empty-1">{$row["Titulo"]}</legend>
                                <p><a href="album?idAlbum=$idAlbum" class="icon-folder-open-empty-1">Álbum {$row["IdAlbum"]}</a></p>
                                <p class="icon-feather">Descripción: {$row["Descripcion"]}</p>
                            </fieldset> 
                        </footer>
                    </figure>
                    hereDOC;
                }
            ?>
        </aside>
        <?php
        /*
        echo <<<hereDOC
        <img src="controller/carpeta.php">
    hereDOC;*/
      ?>
    </section>
</main>
<?php    
    require_once('view/inicio.php');
?>
<?php    
    require_once('view/pie.php');
?>