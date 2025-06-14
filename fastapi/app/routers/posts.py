from fastapi import APIRouter, Depends
from sqlalchemy import text
from pydantic import BaseModel
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

class Post(BaseModel):
    id: int
    title: str
    content: str

@router.get("/", response_model=list[Post])
def list_posts(db=Depends(get_db)):
    result = db.execute(text("SELECT ID, post_title, post_content FROM wp_posts WHERE post_status='publish'"))
    return [Post(id=row[0], title=row[1], content=row[2]) for row in result]
