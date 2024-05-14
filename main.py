import json
import phpbb_extractor
import vbulletin_extractor


def main():
    url = "https://www.phpbb.com/community/viewtopic.php?f=46&t=2159437"
    posts_arr = phpbb_extractor.scrape_phpbb_posts(url)
    my_dict = convert_to_dict(posts_arr)
    with open('phpbbPosts.json', 'w') as json_file:
        json.dump(my_dict, json_file, indent=4)

    url = "https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting" \
          "/414325-www-vs-non-www-url-causing-site-not-to-login"
    posts_arr = vbulletin_extractor.scrape_vbulletin_post(url)
    my_dict = convert_to_dict(posts_arr)
    with open('vbulletin_posts.json', 'w') as json_file:
        json.dump(my_dict, json_file, indent=4)


def convert_to_dict(posts_arr):
    i = 0
    my_dict = {}
    for post in posts_arr:
        i += 1
        print(f'post number {i}: {post.to_dict(i)}')
        my_dict.update({i: post.to_dict(i)})
    print(my_dict)
    return my_dict


if __name__ == "__main__":
    main()
