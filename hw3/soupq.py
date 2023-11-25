import re
from bs4 import BeautifulSoup

html = '''
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
<li>To learn HTML</li>
<li>
To show off
<ol>
<li>To my boss</li>
<li>To my friends</li>
<li>To my cat</li>
<li>To the little talking duck in my brain</li>
</ol>
</li>
<li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h2>Where to find the tutorial</h2>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h3>Some random table</h3>
<table>
<tr class="tutorial1">
<td>Row 1, cell 1</td>
<td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
<td>Row 1, cell 3</td>
</tr>
<tr class="tutorial2">
<td>Row 2, cell 1</td>
<td>Row 2, cell 2</td>
<td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
</tr>
</table>
</body>
</html>
'''
bs = BeautifulSoup(html, 'html.parser')
#a. [4 points]. The title of the HTML page. Use the HTML tags to do this search.
print(bs.find('title').get_text())
#b. [4 points]. The second list item element "li" below "To show off"? Use the HTML tags to do this
#               search. The output should be "To my friends".
#target = re.compile('To')
#print(re.search('To show off', html).string)
print(bs.find('ul').find('ol').find('li').find_next_sibling('li').get_text())
#c. [4 points]. All cells of Row 2. Use the HTML tags to do this search.
print(bs.find('tr', {'class':'tutorial2'}).find_all('td'))
#d. [4 points]. All h2 headings that includes the word “tutorial”. Use the HTML tags to do this search.
print([tag.get_text() for tag in bs.find_all('h2', string=re.compile(".*tutorial.*"))])
#e. [4 points]. All text that includes the “HTML” word. Use the HTML text to do this search.
print(bs.find_all(string=re.compile('.*HTML.*')))
#f. [4 points]. All cells’ data from the first row of the table. Use the HTML tags to do this search.
print([tag.get_text() for tag in bs.find('tr', {'class':'tutorial1'}).find_all('td')])
#g. [4 points]. All images from the table. Use the HTML tags to do this search.
print(bs.find('table').find_all('img'))

