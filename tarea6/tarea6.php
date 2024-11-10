<h1>Tarea 6</h1>
<?php
$equipos = array(
    array("La Paz", "Bolìvar", 20000),
    array("Oruro", "San José", 5000),
    array("Santa Cruz", "Oriente", 25000)
);

echo "<table border='1' cellspacing='0'>";
echo "<caption>Equipos</caption>";

for ($i = 0; $i < count($equipos); $i++) {
    echo "<tr>";
    for ($j = 0; $j < count($equipos[$i]); $j++) {
        echo "<td>" . $equipos[$i][$j] . "</td>";
    }
    echo "</tr>";
}

echo "</table>";
echo "<br>";
?>
