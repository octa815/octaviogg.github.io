<?php
$error = isset($_GET["error"]) ? $_GET["error"] : null;

if ($error == 1) {
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Por favor, no dejes campos en blanco</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}
if ($error == 2){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>asegúrate de que las contraseñas coincidan.</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}
if ($error == 3){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Usuario y/o contraseña incorrectos</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}
if ($error == 4){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>No se encontraron resultados</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}

if ($error == 5){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Edad no valida, debes ser mayor de 18</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}

if ($error == 6){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Email incorrecto, no olvides @ y .</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}

if ($error == 7){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Tienes mas de 100 años?</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}

if ($error == 8){
    echo <<<hereDoc
<main id=pag_error>
    <aside>
        <fieldset >
        <legend class="error_pag">PELIGRO!!</legend>
        <p>Debes escribir un título a tu nuevo album</p>
        </fieldset>
    </aside>
</main>
hereDoc;
}
?>