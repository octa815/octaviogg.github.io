<?php
  if (!isset($_COOKIE["usuario"])){
      include('view/cabecera.php');
  }else{
      include("view/cabecera_privada.php");
  }
  if(isset($_COOKIE["usuario"])) {
    $usuarioActual = $_COOKIE["usuario"];
  }
  include('model/conexion.php');
  include('model/album.php');
?>
<main>
<section id=album>
  
  <?php
  $albumesUsuario = array();
  while ($filaAlbum = mysqli_fetch_assoc($alb)) {
      $albumesUsuario[] = $filaAlbum['IdAlbum'];
  }

  if (!empty($albumes)) {
    foreach ($informacion as $fila) {
    echo <<<hereDOC
    <h2> 
        <fieldset class="icon-folder-open-empty-1">
            {$fila["tituloalbum"]}
        </fieldset>
    </h2>
    <aside class=info>
        <figure>
            <footer>
                <fieldset>
                    <legend class="icon-user-circle-o">{$fila["NomUsuario"]}</legend>
                    <p>Número de fotos en el álbum: {$fila["numfoto"]}</p>
                    <p>Paises donde aparecen las fotos: {$fila["paises"]}</p>
                    <p>Fecha antigua: {$fila["fecha_antigua"]}</p>
                    <p>Fecha actual: {$fila["fecha_reciente"]}</p>
                    <p>{$fila["descalbum"]}</p>
hereDOC;
    // Verificar si el IdAlbum está entre los álbumes del usuario
    if (in_array($fila['idAlbum'], $albumesUsuario)) {
        echo <<<hereDOC
            <a href="anyadirFoto?idAlbum={$fila['idAlbum']}">Añadir foto al álbum {$fila['idAlbum']}</a> 
hereDOC;
    }

    echo <<<hereDOC
                </fieldset> 
            </footer>
        </figure>
    </aside>
hereDOC;
}
 }else {
  echo <<<hereDOC
  <fieldset>
    <p>No se encontraron resultados para este álbum.</p>
  </fieldset> 
  hereDOC;
 }
?>
 <aside class=fotos>
    <?php
   foreach ($albumes as $row) {

    if (!isset($_COOKIE["usuario"])){
      echo <<<hereDOC
      <figure>
      <a href="mensaje_error"><img src="{$row["Fichero"]}"></a>
      hereDOC;
    }else{
      echo <<<hereDOC
      <figure>
      <a href="detalle?idFoto={$row['IdFoto']}"><img src="{$row["Fichero"]}"></a>
      hereDOC;
    }
    echo <<<hereDOC
          <footer>
            <fieldset>
            <legend class="icon-picture">{$row["titulofoto"]}</legend>
              <p class="icon-globe">{$row["NomPais"]}</p>
              <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
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
<?php    
  require_once('view/pie.php');
?>