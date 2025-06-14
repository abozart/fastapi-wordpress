import graphene
from sqlalchemy import text
from .database import get_db

class Post(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    content = graphene.String()

class Query(graphene.ObjectType):
    posts = graphene.List(Post)

    def resolve_posts(self, info):
        db = info.context['db']
        result = db.execute(text("SELECT ID, post_title, post_content FROM wp_posts WHERE post_status='publish'"))
        return [Post(id=row[0], title=row[1], content=row[2]) for row in result]

schema = graphene.Schema(query=Query)
