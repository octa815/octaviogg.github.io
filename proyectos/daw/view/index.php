
<?php
    if (!isset($_COOKIE["usuario"])){
        include('view/cabecera.php');
    }else{
        include("view/cabecera_privada.php");
    }

    include('model/conexion.php');
    include('model/index.php');
?>
    <section id="principal">
        <fieldset>
            <h2 class="icon-picture"> FOTOS </h2>
        </fieldset>
        <article>  
            <?php
            if (isset($_COOKIE['usuario'])){
                while($fila = mysqli_fetch_assoc($principal)){
                    echo <<<hereDOC
                    <a href="detalle?idFoto={$fila['IdFoto']}">
                    <img src="{$fila['Fichero']}" alt="{$fila['Alternativo']}" class="imagenes">
                     </a>
hereDOC;
                }  

            }else{
                while($fila = mysqli_fetch_assoc($principal)){
                echo <<<hereDOC
                <a href="mensaje_error">
                <img src="{$fila['Fichero']}" alt="{$fila['Alternativo']}" class="imagenes">
                 </a>
hereDOC;
                }
            }
            ?>
        </article>
    </section>
    <section id="secundaria">
<fieldset>
    <h3> Fotos más actuales </h3>
</fieldset>
 <aside>
<?php
 if (!isset($_COOKIE["usuario"])){
    while($row = mysqli_fetch_assoc($result)){
        echo <<<hereDOC
        <figure>
            <fieldset class="icon-picture">
                {$row["Titulo"]}
            </fieldset> 
            <a href="mensaje_error"><img src="{$row["Fichero"]}" alt="{$row["Alternativo"]}"></a>
            <footer>
                <fieldset>
                    <legend class="icon-user-circle-o">{$row["NomUsuario"]}</legend>
                    <p class="icon-globe">{$row["NomPais"]}</p>
                    <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                    <p class="icon-feather">{$row["Descripcion"]}</p>
                </fieldset> 
            </footer>
        </figure>
    hereDOC;
    }
}else{
    while($row = mysqli_fetch_assoc($result)){
        echo <<<hereDOC
        <figure>
            <fieldset class="icon-picture">
                {$row["Titulo"]}
            </fieldset> 
            <a href="detalle?idFoto={$row['IdFoto']}"><img src="{$row["Fichero"]}" alt="{$row["Alternativo"]}"></a>
            <footer>
                <fieldset>
                    <legend class="icon-user-circle-o">{$row["NomUsuario"]}</legend>
                    <p class="icon-globe">{$row["NomPais"]}</p>
                    <p class="icon-calendar">Fecha: {$row["Fecha"]}</p>
                    <p class="icon-feather">{$row["Descripcion"]}</p>
                </fieldset> 
            </footer>
        </figure>
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
<script>
    scroll();
</script>
<?php    
    require_once('view/pie.php');
?>
   
   