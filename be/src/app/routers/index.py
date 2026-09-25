from fastapi import APIRouter

from app.http.errors import PROBLEM_RESPONSES
from app.schemas.responses import MessageData, Success

router = APIRouter()


@router.get("/", responses=PROBLEM_RESPONSES)
def index() -> Success[MessageData]:
    return Success(data=MessageData(message="Hello, API!"))
