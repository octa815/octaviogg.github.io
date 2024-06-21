<?php
  include("view/cabecera_privada.php");
  include('model/conexion.php');
?>

<main>
  <aside>
    <fieldset >
    <legend class="icon-upload-cloud">SUBE TUS FOTOS</legend>   
      <form action="res_foto" method="post" id="anyadir">
      <h2> Añade tus fotos </h2>
        <aside id="subir"> 
            <p>
              <label for="titulo" class="icon-feather">Titulo: </label>
            </p>   
            <p>
              <input type="text" id="titulo" name="titulo">
              <span id="errorNombreUsuario" class="error"></span>
            </p>   
            <p>
            <label for="descripción"  class="icon-comment">Descripción: </label>
            </p>   
            <p>
            <textarea id="desc" name="descripcion" placeholder="Deidcatoria o descripción" maxlength="4000"></textarea>
            </p>                    
            <p>
              <label for="nombre" class="icon-calendar">Fecha: </label>
            </p>   
            <p>
              <input type="date" id="fecha" name="fecha">
              <span  class="error"></span>
            </p>
        </aside>
        <aside id="bajar">
            <p>
              <label for="pais" class="icon-globe">País: </label>
              <select id="pais" name="pais">
                <?php
                    include('model/pais.php');
                ?>
              </select>
            </p>
                <label for="foto" class="icon-upload-cloud">Foto: </label>
                <input type="file" accept="image/jpg, image/png, image/gif, image/jpeg" id="input-image" name="foto">                        
            </p>
            <p>
            <label for="alternativo" class="icon-comment">Texto alternativo: </label>
            </p>   
            <p>
            <textarea id="alternativo" name="alternativo" placeholder="Deidcatoria o descripción" maxlength="4000"></textarea>
            </p> 
            <p>
              <label for="album" class="icon-folder-open-empty-1">Álbum: </label>
              <select  name="album">
                <?php
                include('model/selectalbum.php');
                ?>
              </select>
            <p>          
              <button type="submit">Subir foto</button>
              <button type="reset">Borrar</button>    
        </aside>
      </form>
    </fieldset>    
  </aside>
</main>

<!--************************************************************************************-->
<?php    
    require_once('view/inicio.php');
?>
<!--************************************************************************************-->
<?php    
  require_once('view/pie.php');
?>