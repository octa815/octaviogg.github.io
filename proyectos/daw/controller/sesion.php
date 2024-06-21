<?php
    session_start();
    /******************************************GALLETAS*******************************************/
    $usu = $_COOKIE["usuario"];
    $visita = isset($_COOKIE["ultima_visita"]) ? $_COOKIE["ultima_visita"] : "Nunca";
    $recordar = isset($_POST['remember']) && $_POST['remember'] == "on";
    if (!$recordar) {
        if (!isset($_SESSION['primer_acceso'])) {
            $mensaje = "Bienvenido de nuevo, $usu! Su última visita fue: $visita";
            $_SESSION['guardausu'] = $visita;
            setcookie("ultima_visita", date("Y-m-d H:i:s"), time() + 90 * 24 * 60 * 60);
            $_SESSION['primer_acceso'] = false; 
        }else{
            $guardavis = $_SESSION['guardausu'];
            $mensaje = "Su última visita fue: $guardavis";
        }
    } else {
        setcookie("usuario", "", time() - 3600);
        setcookie("psw", "", time() - 3600);
        setcookie("ultima_visita", "", time() - 3600);
        $mensaje = "Adiós. Sus cookies se han eliminado al cerrar el navegador.";
    }
    $hora_actual = date('H:i');
    $manana_inicio = '06:00';
    $manana_fin = '11:59';
    $tarde_inicio = '12:00';
    $tarde_fin = '15:59';
    $tarde_noche_inicio = '16:00';
    $tarde_noche_fin = '19:59';
    $saludo = '';
    if ($hora_actual >= $manana_inicio && $hora_actual <= $manana_fin) {
        $saludo = "Buenos días";
    } elseif ($hora_actual >= $tarde_inicio && $hora_actual <= $tarde_fin) {
        $saludo = "Hola";
    } elseif ($hora_actual >= $tarde_noche_inicio && $hora_actual <= $tarde_noche_fin) {
        $saludo = "Buenas tardes";
    } else {
        $saludo = "Buenas noches";
    } 
    /*********************************************************************************************/
?>