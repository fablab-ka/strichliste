<head>
    <title>Strichliste</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">

</head>
<meta http-equiv="refresh" content="20; URL=/">
<body>

<h1>Hallo {{customer.name}}, dein Kontostand beträgt {{"{:.2f}".format(customer.get_credit())}}€ Was willst du kaufen?</h1>
<div class="box_container">
%for product in products:
<a href="/product/{{product.get_id()}}">
<div class="box">
    {{product.name}}
    <br>
    {{"{:.2f}".format(-product.price)}}€
</div>
</a>
%end
</div>

<input class="btn" type="button" onclick="location.href='/'" value="Zurück">
<input class="btn" style="width:300px" type="button" onclick="location.href='/cash_payin'" value="Geld einzahlen">


<form action="/product_barcode" method="post">
    <input style="display:none" id="barcode" type="number" name="barcode">
</form>
<script language="javascript" type="text/javascript" src="/static/js/barcode.js"></script>


</body>
</html>