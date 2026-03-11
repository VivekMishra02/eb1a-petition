import requests
from bs4 import BeautifulSoup
from weasyprint import HTML

url = 'https://voyagela.com/interview/rising-stars-meet-vivek-mishra-of-long-beach/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
print("Fetching URL...")
response = requests.get(url, headers=headers)
html_content = response.text

print("Parsing HTML...")
soup = BeautifulSoup(html_content, 'html.parser')
# keep only main content to make it clean
article = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
if not article:
    article = soup.body

# create a clean HTML wrapper
clean_html = f"""
<html>
<head>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
img {{ max-width: 100%; height: auto; }}
h1 {{ color: #222; }}
</style>
</head>
<body>
<h1>VoyageLA: Rising Stars: Meet Vivek Mishra of Long Beach</h1>
<p><i>Source: {url}</i></p>
<hr>
{article.prettify()}
</body>
</html>
"""

print("Generating PDF...")
HTML(string=clean_html, base_url=url).write_pdf('/Users/vivekmishra/Downloads/eb1_template/criteria/media/evidence/VoyageLA_Interview.pdf')
print("Done!")
