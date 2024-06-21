function scroll(){
  var myIndex = 0;
  carousel();
  
  function carousel() {
    var i;
    var x = document.getElementsByClassName("imagenes");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";  
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}    
    x[myIndex-1].style.display = "block";  
    setTimeout(carousel, 5000);    
  }
}

function login(){
  var modal = document.getElementById('login');

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}

function registro(){
  var modal2 = document.getElementById('registro');

  window.onclick = function(event) {
    if (event.target == modal2) {
      modal2.style.display = "none";
    }
  }
}


function openNav() {
  document.getElementById("panel").style.width = "250px";
}
  
function closeNav() {
  document.getElementById("panel").style.width = "0";
}

function oscuro() {
  var element = document.body;
  element.classList.toggle("dark-mode");
}

function grande() {
  var element = document.body;
  element.classList.toggle("grande-mode");
}
  
/*---------------FUNCIONES FORMULARIOS Y TABLA----------------------------------------------------------------------------*/
/*----con esta funcion nos ahorramos poner document.getElementbyId--------------------------------------------------------
function $(id) {
  return document.getElementById(id);
  }*/

/*CARGAR-----------------------------------------------------------------------------------------------------------------

function load() {
  document.getElementsByName('loginForm')[0].addEventListener("submit", validaLogin);
  document.getElementsByName('registroForm')[0].addEventListener("submit", validaRegistro);
}
document.addEventListener("DOMContentLoaded", load, false);*/

/*VALIDAR LOGIN-----------------------------------------------------------------------------------------------------------
function validaLogin(event) {
  
  var ok = true;
  var msg = "Debes escribir algo en los campos:\n";
  var nombre = document.getElementsByName('loginForm')[0].nombre.value;
  var pass = document.getElementsByName('loginForm')[0].pass.value;

  var val_nombre = /^[a-zA-Z][a-zA-Z0-9]{2,14}$/;
  var val_pass = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,15}$/;*/

  /*ERRORES ONLINE-----------------------------------------------------------------------------------------------------
  var errorNombre = $('errorNombreUsuario');
  var errorPass = $('errorPass');

  if(!val_nombre.test(nombre)){
    errorNombre.textContent='Necesitas introducir nombre';
    ok = false;
  }else{
    errorNombre.textContent='';
  }

  if (!val_pass.test(pass) ) {
    errorPass.textContent='Introduce una contraseña correcta';
    ok = false;
  }else{
    errorPass.textContent='';
  }

  if (ok == false) {
    event.preventDefault();
  } else {
    alert("Todo correcto, se envía el formulario");
  }
}*/
/*VALIDAR REGISTRO--------------------------------------------------------------------------------------------------------

function validaRegistro(event) {
  
  var ok = true;

  var nombre = document.getElementsByName('registroForm')[0].nombre_reg.value;
  var pass = document.getElementsByName('registroForm')[0].pass_reg.value;
  var rep_pass = document.getElementsByName('registroForm')[0].pass2.value;
  var email = document.getElementsByName('registroForm')[0].email_reg.value;
  var hombre = $('masculino').checked;
  var mujer = $('femenino').checked;
  var email = document.getElementsByName('registroForm')[0].email_reg.value;
  var fecha = document.getElementsByName('registroForm')[0].fecha1.value;*/

  
/*VALIDACIONES-----------------------------------

  var val_nombre = /^[a-zA-Z][a-zA-Z0-9]{2,14}$/;
  var val_pass = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,15}$/;
  var val_email = /^(?!^\.)(?!.\.$)(?!.\.\.)[a-zA-Z0-9!#$%&'+\-/=?^_`{|}~]+(\.[a-zA-Z0-9!#$%&'+\-/=?^_`{|}~]+)@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)(\.[a-zA-Z]{2,})$/;
  

  var val_fecha = /^\d{4}-\d{2}-\d{2}$/; //FORMATO FECHA

  var errorNombre = $('errorNombre_reg');
  var errorPass = $('errorPass_reg');
  var errorPass2 = $('errorPass2');
  var errorMail = $('errorMail_reg');
  var errorEMail= $('errorEMail_reg');
  var errorSexo = $('errorSexo_reg');
  var errorFecha = $('errorFecha_reg');
  var errorNac = $('errorNac_reg');

  if(!val_nombre.test(nombre)){
    errorNombre.textContent='Necesitas introducir nombre';
    ok = false;
  }else{
    errorNombre.textContent='';
  }

  if (!val_pass.test(pass) ) {
    errorPass.textContent='Introduce una contraseña correcta';
    ok = false;
  }else{
    errorPass.textContent='';
  }

  if (rep_pass != pass ) {
    errorPass2.textContent='No coicide con contraseña';
    ok = false;
  }else{
    errorPass2.textContent='';
  }
  if (!val_email.test(email) ) {
    errorMail.textContent='Introduce un mail correcto';
    ok = false;
  }else{
    errorMail.textContent='';
  }
  if (email.length>254){
    errorEMail.textContent='email no puede superar 254 caracteres';
    ok = false;
  }else{
    errorEMail.textContent='';
  }*/

  /*
  if (!hombre && !mujer) {
    errorSexo.textContent = 'Selecciona un sexo.';
    ok = false;
  } else {
    errorSexo.textContent = '';
  }

  if (!val_fecha.test(fecha)) {
    errorFecha.textContent = 'Formato fecha incorrecto';
    ok = false;
  }else {
    errorFecha.textContent = '';
  }


  var fechaActual = new Date();        //fecha de hoy
  var fechaNac = new Date(fecha);     //fecha nacimiento
  var edad = fechaActual.getFullYear() - fechaNac.getFullYear();
  console.log(edad);
  console.log(fechaActual.getFullYear());
  console.log(fechaNac.getFullYear());

  if (fechaActual.getMonth() < fechaNac.getMonth() || (fechaActual.getMonth() == fechaNac.getMonth() && fechaActual.getDate() < fechaNac.getDate())) {
    edad--;
  }

  if (edad < 18) {
    errorNac.textContent = 'Debes tener al menos 18 años para registrarte.';
    ok = false;
  } else {
    errorNac.textContent = '';
  }
 
  if (ok == false) {
    event.preventDefault();
  } else {
    alert("Todo correcto, se envía el formulario");
  }
}*/


/*CÁLCULO--------------------------------------------------------------------------------------------------------------

let costoTotalGlobal = 0;

document.addEventListener('DOMContentLoaded', function()  {*/

    /*Cogemos los datos 
  const copiasInput = $('copias');
  const impresionCheckbox = $('impresion');
  const resolucionInput = $('res');
  const fotosInput = $('numFotos');

  // Asegúrate de que costoElement sea un elemento válido en tu HTML
  const costoElement = document.getElementById('costo');*/

  /*Detectar cambios en el formulario
  copiasInput.addEventListener('input', calculateCost);
  impresionCheckbox.addEventListener('change', calculateCost);
  resolucionInput.addEventListener('input', calculateCost);
  fotosInput.addEventListener('input', calculateCost);*/
  
  /*Calcular el gasto

  function calculateCost() {
    // Obtén los valores de los elementos y los conviertes a números (si es necesario)
    const numCopias = parseInt(copiasInput.value);
    const impresionColor = impresionCheckbox.checked;
    const resolucion = parseFloat(resolucionInput.value);
    const numFotos = parseFloat(fotosInput.value);

    // Realizar cálculos basados en los valores del formulario
    let costoTotal = 0;
    console.log(numCopias);
    console.log(impresionColor);
    console.log(resolucion);
    console.log(numFotos);

    if (numCopias >0 && numCopias < 5){
      costoTotal += numCopias * 0.10;
    } 
    else if (numCopias >4 && numCopias < 11){
      costoTotal += numCopias * 0.08 + 0.08;
    }
    else if (numCopias >= 11){
      costoTotal += numCopias * 0.07 + 0.19;
    }
    if (impresionColor) {
      costoTotal += numFotos * 0.05;
    }
    if (resolucion > 300) {
      costoTotal += numFotos * 0.02;
    }

    costoTotalGlobal = costoTotal;

    // Muestra el costo total en el elemento HTML
    costoElement.textContent = `Costo Total: ${costoTotal.toFixed(2)} €`;

    //return costoTotal;

  }
});*/
/*AÑADIR Y BORRAR FILAS-------------------------------------------------------------------------------------------------
function anyadir() {


  const impresionCheckbox = $('impresion');
  let impresionColor = impresionCheckbox.checked;
  if (impresionColor) {
    $("impresion").value = "si";
  }else{
    $("impresion").value = "no";
  }

  var tabla = document.createElement("table");
  
    for(f = 0; f < 1; f++) {
      var fila = tabla.insertRow();
      for(c = 0; c < 5; c++) {
        var celda = fila.insertCell();
        if(c==0){
          celda.textContent = $("copias").value;  
        }
        if(c==1){
          celda.textContent = $("numFotos").value;  
        }
        if(c==2){
          celda.textContent = $("impresion").value;  
        }
        if(c==3){
          celda.textContent = $("res").value;  
        }     
        if(c==4){
          celda.textContent = costoTotalGlobal.toFixed(2) + " €";  
        }  
      }
    } 
  $("mitabla").appendChild(tabla);
  }

  function borrar(){
   let fila = $("mitabla");
    if (fila.hasChildNodes()) {
      fila.removeChild(fila.lastChild);
  }
}*/
