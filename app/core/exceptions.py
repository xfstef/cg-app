from json import dumps
from typing import Any, Dict, Optional

from fastapi import HTTPException as FastAPIHTTPException
from fastapi import status as http_status


class HTTPExceptionDetails:
    variants = {"warning", "error", "default", "success", "info"}
    anchor_verticals = {"bottom", "top"}
    anchor_horizontals = {"left", "center", "right"}
    action_types = {"link", "verify_email", "verify_phone"}

    def __init__(
            self,
            title: str = "",
            description: str = "",
            permanent: bool = False,
            variant: str = "default",
            anchor_vertical: str = "bottom",
            anchor_horizontal: str = "left",
            action_type: str = "link",
            button_text: str = ""
    ):
        self.title = title
        self.description = description
        self.permanent = permanent
        self.variant = variant
        self.anchor_vertical = anchor_vertical
        self.anchor_horizontal = anchor_horizontal
        self.action_type = action_type
        self.button_text = button_text

        self.validate()

    @property
    def dict(self):
        details = {
            "message": {
                "title": self.title,
                "description": self.description
            },
            "description": self.description,
            "options": {
                "permanent": self.permanent,
                "variant": self.variant,
                "anchorOrigin": {
                    "vertical": self.anchor_vertical,
                    "horizontal": self.anchor_horizontal
                },
                "action": {
                    "type": self.action_type,
                    "buttonText": self.button_text
                }
            }
        }

        return details

    @property
    def json(self):
        details = self.dict
        return dumps(details, indent=2)

    def validate(self):
        if self.variant not in self.variants:
            raise ValueError(
                f"The variant for HTTPException must one of: {self.variants}"
            )

        if self.anchor_vertical not in self.anchor_verticals:
            raise ValueError(
                f"The anchor vertical for HTTPException "
                f"must one of: {self.anchor_verticals}"
            )

        if self.anchor_horizontal not in self.anchor_horizontals:
            raise ValueError(
                f"The anchor horizontal for HTTPException "
                f"must one of: {self.anchor_horizontals}"
            )

        if self.action_type and self.action_type not in self.action_types:
            raise ValueError(
                f"The action_type for HTTPException "
                f"must one of: {self.action_types}"
            )


class HTTPException(FastAPIHTTPException):
    def __init__(
            self,
            status_code: int,
            title: str = "",
            description: str = "",
            permanent: bool = False,
            variant: str = "default",
            anchor_vertical: str = "bottom",
            anchor_horizontal: str = "left",
            action_type: str = "link",
            button_text: str = "",
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        detail = HTTPExceptionDetails(
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text
        )

        super().__init__(status_code=status_code, detail=detail.dict)
        self.headers = headers


class HTTP403(HTTPException):
    def __init__(
            self,
            title: str = "Access is forbidden!",
            description: str = "",
            permanent: bool = True,
            variant: str = "error",
            anchor_vertical: str = "top",
            anchor_horizontal: str = "center",
            action_type: str = None,
            button_text: str = None,
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=http_status.HTTP_403_FORBIDDEN,
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text,
            headers=headers
        )


class HTTP403UsernameExists(HTTP403):
    def __init__(self):
        super().__init__(
            title="Good news!",
            description="The username is already registered. "
                        "Please try to register with a different one!"
        )


class HTTP403PostTitleExists(HTTP403):
    def __init__(self):
        super().__init__(
            title="Post exists!",
            description="A Post with the same title already exists. "
                        "Please try a different title!"
        )


class HTTP403SubscriptionExists(HTTP403):
    def __init__(self):
        super().__init__(
            title="Subscription exists!",
            description="A Subscription to the same author exists. "
                        "Please try a different author!"
        )


class HTTP403SubscriptionDoesNotExist(HTTP403):
    def __init__(self):
        super().__init__(
            title="Subscription does not exist!",
            description="A Subscription to the same author does not exist. "
                        "Please try a different author!"
        )


class HTTP403SubscriptionsLimit(HTTP403):
    def __init__(self):
        super().__init__(
            title="Subscription limit reached!!",
            description="You have reached your 100 Subscriptions limit. "
                        "Please remove some subscriptions first!"
        )


class HTTP404(HTTPException):
    def __init__(
            self,
            title: str = "The item hasn't been found!",
            description: str = "",
            permanent: bool = False,
            variant: str = "default",
            anchor_vertical: str = "bottom",
            anchor_horizontal: str = "left",
            action_type: str = "link",
            button_text: str = "",
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=http_status.HTTP_404_NOT_FOUND,
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text,
            headers=headers
        )


class HTTP409(HTTPException):
    def __init__(
            self,
            title: str = "Conflict!",
            description: str = "",
            permanent: bool = True,
            variant: str = "error",
            anchor_vertical: str = "top",
            anchor_horizontal: str = "center",
            action_type: str = None,
            button_text: str = None,
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=http_status.HTTP_409_CONFLICT,
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text,
            headers=headers
        )


class HTTP415(HTTPException):
    def __init__(
            self,
            title: str = "Unsupported media type!",
            description: str = "",
            permanent: bool = True,
            variant: str = "error",
            anchor_vertical: str = "top",
            anchor_horizontal: str = "center",
            action_type: str = None,
            button_text: str = None,
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text,
            headers=headers
        )


class HTTP503(HTTPException):
    def __init__(
            self,
            title: str = "The service is unavailable!",
            description: str = "",
            permanent: bool = True,
            variant: str = "error",
            anchor_vertical: str = "top",
            anchor_horizontal: str = "center",
            action_type: str = None,
            button_text: str = None,
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
            title=title,
            description=description,
            permanent=permanent,
            variant=variant,
            anchor_vertical=anchor_vertical,
            anchor_horizontal=anchor_horizontal,
            action_type=action_type,
            button_text=button_text,
            headers=headers
        )
