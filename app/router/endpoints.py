from fastapi import APIRouter

from app.auth.api import router as auth
from app.users.api import router as users
from app.posts.api import router as posts
from app.subscriptions.api import router as subscriptions

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (auth, "auth", "auth"),
    (users, "users", "users"),
    (posts, "posts", "posts"),
    (subscriptions, "subscriptions", "subscriptions")
)

for router_item in routers:
   router, prefix, tag = router_item

   if tag:
       include_api(router, prefix=f"/{prefix}", tags=[tag])
   else:
       include_api(router, prefix=f"/{prefix}")
