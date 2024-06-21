<?php    
    require_once('view/cabecera.php');
    include("model/conexion.php");
?>
<?php
$hoy = date("Y-m-d H:i:s");     
$username = $_GET["nombre_reg"];
$apelli = $_GET["apellidos"] ;
$password = $_GET["pass_reg"] ;
$confirm_password = ($_GET["pass2"]);
$email = $_GET["email_reg"];
$sex = isset($_GET["sexo"])? $_GET["sexo"]:'Prefiero no decirlo' ;
$fecha = $_GET["fecha1"];
$ciud = $_GET["ciudad"];
$pas = $_GET["pais"] ;

//********************VALIDACIONES***************/

    if (empty($username) || empty($password) || empty($confirm_password)|| 
    empty($email) || empty($pas) || empty($sex) || empty($fecha) ) {
        header("Location: errores?error=1");
        exit();
    }
    // Validar que las contraseñas coincidan
    if ($password !== $confirm_password) {
        header("Location: errores?error=2"); // password no coinciden
        exit();
    }
  

    // Validar contraseña
    if (!preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d_\-]{6,15}$/', $password) || $password !== $confirm_password) {
        header("Location: errores?error=3"); //contraseña incorrectos
        exit();
    }

    // Validar dirección de email
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        header("Location: errores?error=6"); //email incorrecto
        exit();
    }

    // Validar fecha de nacimiento
    $fecha_actual = date("Y-m-d"); 
    $edad_minima = 18;
    $edad_maxima = 100;
    
    if (strtotime($fecha) === false || strtotime($fecha) > strtotime("-$edad_minima years", strtotime($fecha_actual))) {
        header("Location: errores?error=5"); // error edad
        exit();
    }

    if (strtotime($fecha) === false || strtotime($fecha) < strtotime("-$edad_maxima years", strtotime($fecha_actual))) {
        header("Location: errores?error=7"); // error edad
        exit();
    }

    $insert = "INSERT INTO usuarios VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, NULL, ?, '1')";

    $stmt = mysqli_prepare($connect, $insert);
    mysqli_stmt_bind_param($stmt, "ssssssss", 
        $username, 
        $password, 
        $email, 
        $sex, 
        $fecha, 
        $ciud, 
        $pas, 
        $hoy);
    
    if (!mysqli_stmt_execute($stmt)) {
        die("Error: no se pudo realizar la inserción");
    }
    mysqli_stmt_close($stmt);
    mysqli_close($connect);


echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset id="succes" >
        <legend>ENHORABUENA!!</legend>
        <p>Usuario  creado correctamente con los siguientes datos</p>
        <ul>
        <li>Usuario: $username</li>
        <li>Contraseña: $password</li>
        <li>Contraseña (repetida): $confirm_password</li>
        <li>Apellidos: $apelli</li>
        <li>Email: $email</li>
        <li>Sexo: $sex</li>
        <li>Fecha de nacimiento: $fecha</li>
        <li>Ciudad: $ciud</li>
        <li>País: $pas</li>
        </ul>
        <input type="button"  onclick="location.href='./';"value= "OK" />
        </fieldset>    
    </aside>  
</main>
hereDoc;
?>
<?php    
    require_once('view/inicio.php');
?>
<?php    
    require_once('view/pie.php');
?>



