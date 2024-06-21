<?php
    require_once("view/cabecera_privada.php");
    include('model/conexion.php');
?>
<main id="mainalbum">
    <section id="intro" >
        <fieldset>
        <h2 class="icon-edit"> Solicitud de impresión de álbum </h2>
        </fieldset>
        
    </section>
    <fieldset id="tarifas">
        <legend class="icon-thumbs-up">Tarifas</legend>
        <table>
            <!--<caption>Tarifas</caption>-->
                <tr>
                    <th scope="col">Concepto</th>
                    <th scope="col">Tarifa</th>  
                </tr>
                <tr>
                    <td>&lt; 5 páginas</td>
                    <td>0.10 € por pág.</td>
                </tr>
                <tr>
                    <td>entre 5 y 11 páginas</td>
                    <td>0.08 € por pág.</td>
                </tr>
                <tr>
                    <td>> 11 páginas</td>
                    <td>0.07 € por pág.</td>
                </tr>
                <tr>
                    <td>Blanco y negro</td>
                    <td>0 € por pág.</td>
                </tr>
                <tr>
                    <td>Color</td>
                    <td>0.05 € por foto</td>
                </tr>
                <tr>
                    <td>Resolución > 300 dpi</td>
                    <td>0.02 € por foto</td>
                </tr>    
        </table>
        <h2>Costo del Álbum</h2>
        <table border="1">
            <thead>
                <tr>
                    <th scope="col">    </th>
                    <th scope="col">    </th>
                    <th scope="col" colspan="2">Blanco y negro</th>
                    <th scope="col" colspan="2">Color</th>
                </tr>
                <tr>
                    <th scope="col">Número de páginas</th>
                    <th scope="col">Número de fotos</th>
                    <th scope="col">150-300 DPI</th>
                    <th scope="col">450-900 DPI</th>
                    <th scope="col">150-300 DPI</th>
                    <th scope="col">450-900 DPI</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    require_once("controller/clc_tablaalbum.php");
                ?>
            </tbody>
        </table>
    </fieldset>
    <fieldset id="formulario">
        <legend class="icon-edit">Formulario de solicitud</legend>
        <form action="respuesta_solicitar_album" method="post">
            <aside id="izq">
                <p>
                    <label for="nombre">Nombre: </label>
                    <input type="text" id="nombre" name="nombre" maxlength="200" placeholder="Nombre" >(*)
                </p>
                <p>
                    <label for="titulo">Titulo del album: </label>
                    <input type="text" id="titulo" name="titulo" maxlength="200" placeholder="Cubierta" >(*)
                </p>
                <p>
                    <label for="texto_ad">Texto adicional: </label>
                    <textarea id="texto_ad" name="texto_ad" placeholder="Deidcatoria o descripción" maxlength="4000"></textarea>
                </p> 
                <p>
                    <label for="correo">Correo electrónico: </label>
                    <input type="email" id="correo" name="correo" maxlength="200" placeholder="email@email" >
                </p>
                <p>
                    <label for="direccion">Dirección: </label>
                    <input type="text" id="direccion" name="direccion" placeholder="Calle" >
                
                    <label for="numero">Numero: </label> 
                    <input type="text" id="numero" name="numero" placeholder="Número" size="3" >
                
                    <label for="cp">CP: </label>
                    <input type="text" id="cp" name="cp" maxlength="5" placeholder="CP" size="6" >
                
                    <label for="ciudad">Ciudad </label>
                    <select id="ciudad" name="ciudad">
                        <option value="No seleccionado">Localidad</option>
                        <option value="Alicante">Alicante</option>
                        <option value="Madrid">Madrid</option>
                        <option value="Valencia">Valencia</option>
                    </select>
                
                    <label for="provincia">Provincia </label>
                        <select id="provincia" name="provincia">
                            <option value="No seleccionado">Provincia</option>
                            <option value="Valencia">Valencia</option>
                            <option value="murcia">murcia</option>
                            <option value="Andalucia">Andalucia</option>
                        </select>(*)
                    </p>
            </aside>
            <aside id="der">
                <p>
                    <label for="telefono">Telefono: </label>
                    <input type="tel" id="telefono" name="telefono" placeholder="### ## ## ##" >
                </p>  
                <p>
                    <label for="color_portada">Color de portada:</label>
                    <input type="color" id="color_portada" name="color_portada" value="#000000">
                </p>
                <p>
                    <label for="copias">Número de copias (entre 1 y 99)</label>
                    <input type="number" id="copias" name="copias" min="1" max="99">
                </p> 
                <p>
                    <label for="copias">Número de fotos (entre 1 y 99)</label>
                    <input type="number" id="numFotos" name="numFotos" min="1" max="99">
                </p> 
                <p>
                    <label for="res">Resolución de impresión: </label>
                    <input type="range" id="res" name="res" min="150" max="900" step="150" value="150" onchange="document.getElementById('outres').value=value" list="tickmarks">
                    <output id="outres" name="outres" for="res">150</output>

                    <datalist id = "tickmarks">
                        <option value="150"></option>
                        <option value="300"></option>
                        <option value="450"></option>
                        <option value="600"></option>
                        <option value="750"></option>
                        <option value="900"></option>
                    </datalist>
                </p>  
                <p>
              <label for="album" class="icon-folder-open-empty-1">Álbum: </label>
              <select  name="album">
                <?php
                    include('model/selectalbum.php');
                ?>
              </select>
            <p>  
                <p>
                    <label for="fecha1">Fecha de recepción:</label>
                    <input type="date" id="fecha1" name="fecha1"> Fecha aproximada de recepción
                </p>
                <p>
                    <label for="impresion">Impresión a color?: </label>
                    <input type="checkbox" id="impresion" name="impresion">
                </p>    
                <input type="submit" value="Enviar !" id="env">        
            </aside>
        </form>  
    </fieldset>     
</main>
<?php    
    require_once('view/pie.php');
?>
