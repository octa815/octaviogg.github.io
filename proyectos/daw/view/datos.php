<?php
    include("view/cabecera_privada.php");
?>
<!--************************************************************************************-->
<?php
    include('model/conexion.php');
    include('model/datos.php');
?>
<!--************************************************************************************-->
<main>
    <aside >
        <fieldset id=datos>  
            <legend>TUS DATOS</legend>  
            <aside id=information>
            <h2>MIS DATOS</h2>
            <?php
           while ($row = mysqli_fetch_assoc($result)) {
            echo <<<hereDOC
            <p>Nombre: {$row['NomUsuario']}</p>
            <p>Contraseña: {$row['Clave']}</p>
            <p>Email: {$row['Email']}</p>
            <p>Sexo: {$row['Sexo']}</p>
            <p>Fecha de nacimiento: {$row['FNacimiento']}</p>
            <p>Ciudad: {$row['Ciudad']}</p>
            <p>Pais: {$row['NomPais']}</p>
            <p>Foto: <img src="{$row['Foto']}"></p>
            <p>Fecha de registro: {$row['FRegistro']}</p>
            <p class="icon-folder-open-empty-1">Tus álbumes:</p>
hereDOC;

            // Inicializar $row2 antes del bucle
            $row2 = mysqli_fetch_assoc($res);

            do {
                // Verificar si $row2 no es nulo antes de acceder a sus elementos
                if ($row2) {
                    echo <<<hereDOC
                    <a href=album?idAlbum={$row2['IdAlbum']} >{$row2['Titulo']}</a> ||
hereDOC;

                    // Obtener la siguiente fila dentro del bucle
                    $row2 = mysqli_fetch_assoc($res);
                }
            } while ($row2);

            
            
            echo "</aside>";
            }
            ?>
            <aside id=modificar>
                <form action="res_datos">
                <h2>MODIFICA TUS DATOS</h2>
                <p><label for="nombre_reg">Nombre:</label></p>
                <p>   
                    <input type="text" id="nombre_reg" name="nombre_reg">
                    <span id="errorNombre_reg" class="error"></span>
                </p>
                <p><label>Apellidos: </label></p>
                <p>   
                    <input type="text" id="apellidos" name="apellidos" >
                </p>
                <p><label for="pass_reg">Contraseña: </label></p>
                <p>  
                    <input type="text"  id="pass_reg" name="pass_reg" >
                    <span id="errorPass_reg" class="error"></span>
                </p>
                <p><label for="pass2"> Repite contraseña: </label></p>
                <p>
                    <input type="text"  id="pass2" name="pass2">
                    <span id="errorPass2" class="error"></span>
                </p>
                <p><label for="email_reg">Email: </label></p>
                <p>
                    <input type="text" id="email_reg" name="email_reg" >
                    <span id="errorMail_reg" class="error"></span>
                    <span id="errorEMail_reg" class="error"></span>
                </p>
                <p>Sexo:
                    <input type="radio" id="masculino" name="sexo" value=1 > 
                    <label for="masculino">H</label>
                    <input type="radio" id="femenino"  name="sexo" value=2> 
                    <label for="femenino">M</label>
                    <span id="errorSexo_reg" class="error"></span>
                </p>
                <p><label for="fecha1">Fecha de nacimiento:</label></p>
                <p>
                    <input type="text" id="fecha1" placeholder="aaaa-mm-dd" name="fecha1">
                    <span id="errorFecha_reg" class="error"></span>
                    <span id="errorNac_reg" class="error"></span>
                </p>
                <p>
                    <label for="ciudad">Ciudad: </label>
                    <select id="ciudad" name="ciudad">
                        <option value="Alicante">Alicante</option>
                        <option value="Madrid">Madrid</option>
                        <option value="Valencia">Valencia</option>
                    </select>
                </p>
                <p><label for="pais">País: </label>
                    <select id="pais" name="pais">
                        <?php
                            include('model/pais.php');
                        ?>
                    </select>
                </p> 
                <button type="submit">Modificar</button>
                <button type="reset">Borrar</button>
                </form>
        </aside>
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