from fastapi import FastAPI, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp
from .auth import get_current_user
from .database import get_db
from .rss import generate_rss
from .graphql_schema import schema
from .routers import posts

app = FastAPI(title="Oregon Travel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router, dependencies=[Depends(get_current_user)])

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello, {user}!"}

@app.get("/rss")
def rss_feed(db=Depends(get_db)):
    xml = generate_rss(db)
    return Response(content=xml, media_type="application/rss+xml")


def graphql_context(request):
    return {"db": next(get_db())}

app.add_route("/graphql", GraphQLApp(schema=schema, context_value=graphql_context))

