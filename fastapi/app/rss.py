from feedgen.feed import FeedGenerator
from sqlalchemy import text


def generate_rss(db):
    fg = FeedGenerator()
    fg.title('Oregon Travel Posts')
    fg.link(href='http://localhost', rel='alternate')
    fg.description('Latest travel updates about Oregon')

    posts = db.execute(text("SELECT ID, post_title, post_content, post_date FROM wp_posts WHERE post_status='publish' ORDER BY post_date DESC LIMIT 10"))

    for post in posts:
        fe = fg.add_entry()
        fe.id(str(post.ID))
        fe.title(post.post_title)
        fe.link(href=f'http://localhost/?p={post.ID}')
        fe.description(post.post_content)

    return fg.rss_str(pretty=True)
