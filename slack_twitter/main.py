import logging
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import tweepy

REFRESH_TOKEN = 'VGVReWR3d0lJeFR1YW93MkszSzJWT3gxTlhwTFQtNXBoV3BlMDZVQXc5WFpROjE2Njg4MDc0NjgxNjc6MTowOnJ0OjE'


logger = logging.getLogger(__name__)


class Authorization(BaseModel):
    enterprise_id: Optional[str]
    team_id: str
    user_id: str
    is_bot: bool


class BaseEvent(BaseModel):
    type: str
    event_ts: str
    user: str
    ts: str


class MessageEvent(BaseEvent):
    text: str


class EventType(str, Enum):
    MESSAGE = 'message'
    URL_VERIFICATION = 'url_verification'


class URLVerificationMessage(BaseModel):
    token: str
    challenge: str
    type: str


class EventEnvelope(BaseModel):
    event_id: Optional[str]
    event_time: Optional[int]
    event_context: Optional[str]
    authorizations: Optional[List[Authorization]]
    authed_teams: Optional[List[str]]
    authed_users: Optional[List[str]]
    event: Optional[MessageEvent]
    api_app_id: Optional[str]
    team_id: Optional[str]
    token: str
    challenge: Optional[str]
    type: EventType


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Welcome to slack twitter bot'}


@app.post('/slack_event_callback')
def slack_event_callback(request: EventEnvelope):
    if request.type == EventType.URL_VERIFICATION:
        return request.challenge

    if request.type == EventType.MESSAGE:
        logger(request)
        event: MessageEvent = request.event
        return event.text
    return {}
