import requests
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from haru.utils.db import get_database
from haru.model import User
from haru.model.form import CredentialResponse
from haru.utils.auth import get_current_user, create_token

GOOGLE_OAUTH_VERIFY_URL = "https://oauth2.googleapis.com/tokeninfo"
user_router = APIRouter()


@user_router.post("/authorize/google")
def authorize(credential: CredentialResponse):
    result = requests.get(GOOGLE_OAUTH_VERIFY_URL, params={"id_token": credential.credential})
    if result.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential")

    info = result.json()
    if not info["email_verified"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot use unverified signature email. Please use another account",
        )

    email = info["email"]
    name = info["name"]
    picture = info.get("picture")

    generated_user = {
        "_id": uuid.uuid4().hex,
        "google_email": email,
        "google_name": name,
        "google_picture": picture,
    }
    user = get_database().user.find_one_and_update(
        {"google_email": email},
        update={"$setOnInsert": generated_user},
        return_document=True, # return new document
        upsert=True
    )
    access_token = create_token(user["_id"])
    return {"access_token": access_token, "user": user}


@user_router.get("/user")
def get_user(user: User = Depends(get_current_user)):
    return {"user": user}
