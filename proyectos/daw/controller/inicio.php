<?php
include('model/conexion.php');

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['nombre']) && isset($_POST['pass'])) {
    $usuario = $_POST['nombre'];
    $contrasena = $_POST['pass'];

    // Realizar la consulta sin prevención de inyección SQL
    $result = mysqli_query($connect, "SELECT * FROM usuarios WHERE NomUsuario = '$usuario'");

    if ($result && $result->num_rows > 0) {
        $row = $result->fetch_assoc();

        // Verificar la contraseña usando password_verify
        if ($contrasena == $row['Clave']) {
            // Las credenciales son correctas
            // Asignar las sesiones
            $_SESSION["usuario"] = $usuario;
            $_SESSION["psw"] = $contrasena;
            $_SESSION["estilo"] = $row['Estilo'];

            // Configurar cookies para recordar al usuario durante 90 días
            if (isset($_POST["remember"]) && $_POST["remember"] == "on") {
                setcookie("usuario", $usuario, time() + 90 * 24 * 60 * 60);
                setcookie("psw", $contrasena, time() + 90 * 24 * 60 * 60);
                setcookie("ultima_visita", date("Y-m-d H:i:s"), time() + 90 * 24 * 60 * 60);
                setcookie("estilo", $row['Estilo'], time() + 90 * 24 * 60 * 60);
            } else {
                setcookie("usuario", $usuario);
                setcookie("psw", $contrasena);
                setcookie("ultima_visita", date("Y-m-d H:i:s"));
                setcookie("estilo", $row['Estilo']);
            }
            header('Location: ./'); // Redirigir a página de usuario registrado
            exit();
        } else {
            header('Location: errores?error=1'); 
        }
    } else {
        // Usuario no encontrado
        header('Location: errores?error=4'); // Redirigir con mensaje de error
        exit();
    }
}
?>
