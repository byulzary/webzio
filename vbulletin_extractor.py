import re
import requests
from post import Post
import datetime
from datetime import datetime


def get_quotes_from_content(content):
    pattern = r'<div class="message">(.*?)<'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches


def get_text_from_content(content):
    pattern = r'\t*(.*?)<'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # print(content)
    else:
        print("No match found.")
    return content


def extract_texts(html_content):
    pattern = r'itemprop="text">(.*?)<div class="h-flex-spacer h-margin-top-16'
    match = re.findall(pattern, html_content, re.DOTALL)
    contents = []
    if match:
        contents = match
        # print(contents)
    else:
        print("No match found.")
    quote_text = ''
    text = ''
    text_arr = []
    for content in contents:
        # print(content)
        if '<div class=\"message\"' in content:
            quotes = get_quotes_from_content(content)
            for quote in quotes:
                quote_text += quote
        else:
            text = get_text_from_content(content)
            # print(text)
        text_arr.append(quote_text + '' + text)
        text = ''
        quote_text = ''
    return text_arr


def convert_datetime_vbulletin(datetime_str):
    dt_object = datetime.strptime(datetime_str, "%a %d %b '%y, %I:%M%p")
    formatted_datetime = dt_object.strftime('%Y/%m/%d %I:%M')
    return formatted_datetime


def extract_dates_published(html_content):
    pattern = r'<time\s+itemprop="dateCreated"\s+datetime=\'.*?\'>(.*?)</time>'
    matches = re.findall(pattern, html_content)
    date_arr = []
    for match in matches:
        my_date = convert_datetime_vbulletin(match)
        # print(my_date)
        date_arr.append(my_date)
    return date_arr


def extract_names(html_content):
    pattern = r'<div\s+class="author[^"]*"\s+itemprop="author"[^>]*>.*?<span\s+itemprop="name">(.*?)</span>'
    author_matches = re.findall(pattern, html_content, re.DOTALL)
    authors_arr = []
    if author_matches:
        for author_name in author_matches:
            author_name_clean = re.sub(r'<[^>]+>', '', author_name)
            author_name_clean = re.sub(r'&\w+;', '', author_name_clean)
            authors_arr.append(author_name_clean)
    else:
        print('No authors matched.')
    return authors_arr


def extract_titles(html_content):
    pattern = r'<h1\s+class="main-title js-main-title hide-on-editmode">(.*?)</h1>'
    match = re.search(pattern, html_content)
    titles_arr = []
    title = ''
    if match:
        title = match.group(1).strip()
        # print(title)
    else:
        print("No match found.")
    re_titles = 'Re: ' + title
    return title, re_titles


def scrape_vbulletin_post(url):
    # Fetch HTML content of the webpage
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

    else:
        print("Failed to fetch webpage")
        return None

    text_arr = extract_texts(html_content)
    dates_published_arr = extract_dates_published(html_content)
    names_arr = extract_names(html_content)
    title, re_titles = extract_titles(html_content)
    posts_arr = []
    for i in range(len(names_arr)):
        if i == 0:
            p = Post(title, names_arr[i], dates_published_arr[i], text_arr[i])
            posts_arr.append(p)
        else:
            p = Post(re_titles, names_arr[i], dates_published_arr[i], text_arr[i])
            posts_arr.append(p)

    return posts_arr
