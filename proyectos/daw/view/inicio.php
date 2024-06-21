   <?php
   if (!isset($_COOKIE["usuario"])) {
       $recordar = isset($_GET["remember"]) ? $_GET["remember"] : "";
   
    echo <<<hereDOC
    <aside contenteditable="false">
        <aside id="login" class="modal">
            <form action="inicio.php" class="modal-content animate" name="loginForm" method="post">
                <section id="seccion">
                    <span onclick="document.getElementById('login').style.display='none'" class="close" title="Close Modal">&times;</span>
                    <fieldset>  
                        <legend>DATOS DE ACCESO</legend>  
                        <h3> INICIAR SESIÓN </h3>                        
                        <p>
                            <label for="nombre">Nombre: </label>
                            <input type="text" id="nombre" name="nombre">
                            <span id="errorNombreUsuario" class="error"></span>
                        </p>
                        <p>
                            <label for="pass">Contraseña: </label>
                            <input type="password" id="pass" name="pass">
                            <span id="errorPass" class="error"></span>
                        </p>
                        <p>
                            <label>
                                <input type="checkbox" name="remember" $recordar>
                                Recordar
                            </label>
                        </p>
                        <button type="submit">Iniciar sesión</button>
                        <button type="reset">Borrar</button>
                        <p>
                            <span class="psw">Olvidaste tu <a href="#">contraseña?</a></span>
                        </p>
                    </fieldset>  
                </section>
            </form>
        </aside>
    </aside>
hereDOC;
   } else {
       $usu = $_COOKIE["usuario"];
       $visita = $_COOKIE["ultima_visita"];
   
       echo <<<hereDOC
       <aside contenteditable="false">
           <aside id="login" class="modal">
               <form action="index2" class="modal-content animate" name="loginForm" method="post">
                   <section id="seccion">
                       <span onclick="document.getElementById('login').style.display='none'" class="close" title="Close Modal">&times;</span>
                       <fieldset>  
                           <legend>DATOS DE ACCESO</legend>  
                           <h3> INICIAR SESIÓN </h3>                        
                           <p>Hola <strong>$usu</strong></p>
                           <p>Su último inicio de sesión fue: <strong>$visita</strong></p>
                           <button type="submit">Acceder</button>
                           <button>Salir</button>
                           <a href="?logout">Salir</a>       
                       </fieldset>  
                   </section>
               </form>
           </aside>
       </aside>
   hereDOC;
 }
 
if (isset($_GET['logout'])) {
    // Eliminar las cookies
    setcookie("usuario", "", time() - 3600);
    setcookie("psw", "", time() - 3600);
    setcookie("ultima_visita", "", time() - 3600);

    // Redirigir a la página de inicio o a donde desees después de cerrar sesión
    header('Location: ./');
    exit();
}
?>

    <!--************************************************************************************-->
    <aside contenteditable="false">
        <aside id="registro" class="modal2">
            <form action="res_registro" class="modal2-content animate" name="registroForm" method="get">
                <section id="seccion2">
                    <fieldset>  
                        <legend>TUS DATOS</legend>  
                        <h3> REGISTRO </h3>
                            <p>Introduce tus datos</p>
                            <p><label for="nombre_reg">Nombre:</label>
                                <input type="text" id="nombre_reg" name="nombre_reg">
                                <span id="errorNombre_reg" class="error"></span>
                            </p>
                            <p>
                                <label>Apellidos: </label>
                                <input type="text" id="apellidos" name="apellidos" >
                            </p>
                            <p>
                                <label for="pass_reg">Contraseña: </label>
                                <input type="text"  id="pass_reg" name="pass_reg" >
                                <span id="errorPass_reg" class="error"></span>
                            </p>
                            <p>
                                <label for="pass2"> Repite contraseña: </label>
                                <input type="text"  id="pass2" name="pass2">
                                <span id="errorPass2" class="error"></span>
                            </p>
                            <p><label for="email_reg">Email: </label>
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
                            <p>
                                <label for="fecha1">Fecha de nacimiento:</label>
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
                    </fieldset>   
                </section>
                <section id="foto">
                    <span onclick="document.getElementById('registro').style.display='none'" class="close" title="Close Modal">&times;</span>
                    <fieldset>   
                        <legend>TU FOTO</legend> 
                            <h4>Foto:</h4>
                            <label for="input-image"></label> 
                                <figure>
                                    <img src="./imagenes/user1.jpg" alt="imagen">
                                </figure> 
                            <input type="file" accept="image/jpg, image/png, image/gif, image/jpeg" id="input-image">
                    </fieldset> 
                    <aside id="log">
                        <button type="submit">Registrarse</button>
                        <button type="reset">Borrar</button>
                    </aside>       
                </section> 
            </form> 
        </aside>
    </aside>