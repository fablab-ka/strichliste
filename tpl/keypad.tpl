<head>
    <title>Strichliste</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>
<body>
<h2>Hallo Name!</h2>
<h2>Bitte identifiziere dich mit deiner PIN!</h2>
<form action="/keypad" method="post">
    <input type="text" style="width:300px;height:60px" name="pin" id="pin">

    <table>
        <tr>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 7' value="7"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 8'value="8"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 9' value="9"></td>
        </tr>
        <tr>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 4' value="4"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 5' value="5"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 6' value="6"></td>
        </tr>
        <tr>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 1' value="1"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 2' value="2"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 3' value="3"></td>
        </tr>
        <tr>
            <td><input class="btn key" type="button" value=""></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value += 0' value="0"></td>
            <td><input class="btn key" type="button" onclick='document.getElementById("pin").value = ""' value="⌫"></td>
        </tr>
    </table>

    <input class="btn" type="submit" value="Weiter">
    <input class="btn" type="button" onclick="location.href='/'" value="Zurück">

    <input type="text" style="display:none" value="1" name="">

</form>

<div id="keyboard"></div>

</body>

</html>