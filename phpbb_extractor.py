import re
import requests
from post import Post
import datetime
from datetime import datetime


def phpbb_content_cleaner(content):
    gentag = r'(<\w+>|</\w+>|<img\s+[^>]*>)'
    clean_content = re.sub(gentag, '', content)
    clean_content = clean_content.replace('\n', '')
    clean_content = clean_content.replace('\t', '')
    return clean_content


def format_phpbb_date(date):
    # print(date)
    dt_object = datetime.strptime(date, '%a %b %d, %Y %I:%M %p')

    # Format the datetime object into the desired output format
    formatted_datetime = dt_object.strftime('%Y/%m/%d %I:%M')

    return formatted_datetime


def scrape_phpbb_posts(url):
    # Fetch HTML content of the webpage
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

    else:
        print("Failed to fetch webpage")
        return None
    post_pattern = r'<div class="postbody">(.*?)<div class="back2top">'
    title_pattern = r'<h3 .*?>\s*<a href=".+?">(.+?)</a>\s*</h3>'
    content_pattern = r'<div class="content">(.*?)<div id="\w+" class="signature">'
    date_pattern = r'<time datetime="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})">(.+?)</time>'
    author_pattern = r'<a href=".+?class="username.*?">(.+?)</a>'
    post_arr = []
    posts_match = re.findall(post_pattern, html_content, re.DOTALL)
    i = 0
    for post_match in posts_match:
        # print(f'now working on post number:{i}')
        if i == 0:
            title = re.search(title_pattern, post_match, re.DOTALL).group(1)
        else:
            title = re.search(title_pattern, post_match, re.DOTALL).group(1)
        search = re.search(content_pattern, post_match, re.DOTALL)
        content = search.group(1)
        content = phpbb_content_cleaner(content)
        date = re.search(date_pattern, post_match).group(2)
        formatted_date = format_phpbb_date(date)
        author = re.search(author_pattern, post_match).group(1)
        i += 1
        p = Post(title, author, formatted_date, content)
        post_arr.append(p)
    return post_arr
