<html lang="en">
    <head>
        <meta charset='utf-8'>
        <title>AVR Instruction Set</title>
        <link rel="stylesheet" type="text/css" href="assets/css/style.css">
    </head>
    <body>
        <h1>AVR Instruction Set</h1>
        <div id="content">
            <dl>
            {% for i in inst %}
                <dt><a href="{{ inst[i]['href'] }}">{{ i }} - {{ inst[i]['desc'] }}</a></dt>
            {% endfor %}
            </dl>
        </div>
        <div class="footer">made with &#x2665; by cedric (<a href="//0l.wtf">0l.wtf</a>).</div>
    </body>
</html>

