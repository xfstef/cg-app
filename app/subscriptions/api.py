from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app import User, Subscription
from app.auth.dependencies import get_current_user
from app.core.models import StatusMessage
from app.subscriptions.crud import SubscriptionsCRUD
from app.subscriptions.dependencies import get_subscriptions_crud

router = APIRouter()


@router.post(
    "/add_subscription/{username}",
    response_model=Subscription,
    status_code=http_status.HTTP_201_CREATED
)
async def add_subscription(
        username: str,
        subscriptions: SubscriptionsCRUD = Depends(get_subscriptions_crud),
        user: User = Depends(get_current_user)  # noqa
):
    subscription = await subscriptions.add_subscription(username=username, user_id=user.uuid)

    return subscription


@router.post(
    "/remove_subscription/{username}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_201_CREATED
)
async def remove_subscription(
        username: str,
        subscriptions: SubscriptionsCRUD = Depends(get_subscriptions_crud),
        user: User = Depends(get_current_user)  # noqa
):
    removed = await subscriptions.remove_subscription(username=username, user_id=user.uuid)

    return {"status": removed, "message": "The subscription has been removed!"}
