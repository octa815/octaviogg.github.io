<?php
include('model/conexion.php');
include('model/configurar.php');

// Obtener opciones de estilos desde la base de datos
$opcionesEstilos = array();
while ($row = mysqli_fetch_assoc($result)) {
    $opcionesEstilos[] = $row;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['accion']) && $_POST['accion'] === 'guardar_estilo') {
        // Procesar la acción para guardar el estilo
        if (isset($_POST['estilo'])) {
            $idEstilo = $_POST['estilo'];

            // Guardar la preferencia de estilo en la base de datos
            $usuario = $_COOKIE['usuario'];
            $query = "UPDATE usuarios SET Estilo = '$idEstilo' WHERE NomUsuario = '$usuario'";
            $result = mysqli_query($connect, $query);

            if ($result) {
                // Puedes establecer una cookie para recordar la preferencia del usuario
                setcookie('estilo', $idEstilo, time() + (365 * 24 * 60 * 60));
                // Ejemplo: cookie válida por un año
                // Redirigir o mostrar un mensaje de éxito si es necesario
            } else {
                // Manejar el caso en el que la actualización falla
                echo "Error al actualizar el estilo en la base de datos: " . mysqli_error($connect);
            }
        }
    }
}

include("view/cabecera_privada.php");
?>

<main>
  <fieldset>
    <h2 class="icon-attach">Configurar Estilo</h2>
  </fieldset>

  <fieldset>
    <form method="post" action="configurar">
      <label for="estilo">Selecciona un estilo:</label>
      <select name="estilo" id="estilo">
        <?php
        // Mostrar opciones de estilos desde el array
        foreach ($opcionesEstilos as $opcion) {
          echo "<option value='{$opcion["IdEstilo"]}'>{$opcion["Nombre"]}</option>";
        }
        ?>
      </select>
      <input type="hidden" name="accion" value="guardar_estilo">
      <button type="submit">Guardar</button>
    </form>
  </fieldset>    
</main>

<!--************************************************************************************-->
<?php    
    require_once('view/inicio.php');
?>
<!--************************************************************************************-->
<?php    
  require_once('view/pie.php');
?>