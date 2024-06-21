<?php
   if (!isset($_COOKIE["usuario"]) && !isset($_COOKIE["ultima_visita"])){
    include('view/cabecera.php');
}else{
    include("view/cabecera_privada.php");
}

include('model/conexion.php');
include('model/perfil.php');
?>
<main>
  <fieldset> 
    <h2 class="icon-user-circle-o">Perfil de Usuario</h2>
  </fieldset>
  <section id="perfil"> 
    <aside class="left">
    <?php
      while($row = mysqli_fetch_assoc($result)){
      echo <<<hereDOC
          <fieldset>
            <legend class="icon-user-circle-o">{$row['NomUsuario']}</legend>
            <p><img src="{$row['Foto']}" alt='Foto de Perfil'></p>
            <p>Fecha de Incorporación: {$row['FRegistro']}</p>
          </fieldset> 
  hereDOC;
      if ($row['IdAlbum'] !== null) {
        echo <<<hereDOC
        <fieldset>
          <legend>Listado de Álbumes</legend>
        <ul>
  hereDOC;
        do {
        echo <<<hereDOC
        <a href=album?idAlbum={$row['IdAlbum']} class="icon-folder-open-empty-1">
        <li>{$row['Titulo']}</li>
        </a>
  hereDOC;
        } while ($row = $result->fetch_assoc());
        echo "</ul>";
      } else {
        echo "<p>El usuario no tiene álbumes.</p>";
      }
        echo "</fieldset>";
        }
    ?>
    </aside>
  </section>
</main>
<?php    
    require_once('view/inicio.php');
?>
<!--************************************************************************************-->
<?php    
  require_once('view/pie.php');
?>