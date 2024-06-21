<?php
    include("view/cabecera_privada.php");
?>
<main>
    <fieldset> 
        <h1 class="icon-folder-open-empty-1">ÁLBUM</h1>
    </fieldset>
    <aside id="crealbum">
    <form action="res_album" method="post">
        <fieldset>  
        <legend class="icon-folder-add">CREA TU ÁLBUM</legend>  
                <h3> Nombra y describe tu álbum de fotos </h3>                        
                    <p>
                        <label for="titulo" class="icon-comment">Nombre: </label>
                    </p>
                    <p>
                        <input type="text" id="titulo" name="titulo">
                        <span id="errorNombreUsuario" class="error"></span>
                    </p>
                    <p>
                        <label for="descripción" class="icon-feather">Descripción: </label>
                    </p>
                    <p>
                        <textarea id="desc" name="desc" placeholder="Dedicatoria o descripción" maxlength="4000"></textarea>
                        <span id="errorPass" class="error"></span>
                    </p>        
                <button type="submit">Crear álbum</button>
                <button type="reset">borrar</button>    
        </fieldset> 
    </form> 
    </aside>
    
</main>
<?php
require_once("view/pie.php");
?>