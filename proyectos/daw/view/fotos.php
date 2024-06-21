
<?php
    if (!isset($_COOKIE["usuario"])){
        include('view/cabecera.php');
    }else{
        include("view/cabecera_privada.php");
    }
?>
<!-- *BASE DE DATOS**********************************************************************-->
<?php
    include('model/conexion.php');
    include('model/fotos.php');
?>
<!-- *BASE DE DATOS**********************************************************************-->
<main>
    <section id="secundaria">
    <fieldset>
        <h2 class="icon-picture"> TUS FOTOS </h2>
    </fieldset>
 <aside>
<?php

    while($row = mysqli_fetch_assoc($result)){

      echo <<<hereDOC
      <figure>
          <a href="detalle?idFoto={$row['IdFoto']}"><img src="{$row["Fichero"]}" alt="{$row["Alternativo"]}"></a>
          <footer>
              <fieldset>
                  <legend>{$row["Titulo"]}</legend>
                  <p class="icon-globe">{$row["NomPais"]}</p>
                  <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                  <a href="album?idAlbum={$row['Album']}" class="icon-folder-open-empty-1">Album {$row['Album']}</a>
                  <p class="icon-feather">{$row["Descripcion"]}</p>
              </fieldset> 
          </footer>
      </figure>
  hereDOC;
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
<script>
    scroll();
</script>
<?php    
    require_once('view/pie.php');
?>
   
   