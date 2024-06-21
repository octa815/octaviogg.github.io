<?php
$query = "SELECT 
   IdPais, 
   NomPais 
   FROM 
   Paises";

   $result = $connect->query($query);
   while ($row = $result->fetch_assoc()) {
      echo "<option value='" . $row['IdPais'] . "'>" . $row['NomPais'] . "</option>";
 }
?>