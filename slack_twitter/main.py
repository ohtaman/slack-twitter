from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import tweepy

REFRESH_TOKEN = 'VGVReWR3d0lJeFR1YW93MkszSzJWT3gxTlhwTFQtNXBoV3BlMDZVQXc5WFpROjE2Njg4MDc0NjgxNjc6MTowOnJ0OjE'


class Authorization:
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


class EventType(Enum):
    MESSAGE = 'message'


class URLVerificationMessage(BaseModel):
    token: str
    challenge: str
    type: str


class EventEnvelope:
    event_id: str
    event_time: int
    event_context: str
    authorizations: List[Authorization]
    authed_teams: List[str]
    authed_users: List[str]
    event: BaseEvent
    api_app_id: str
    team_id: str
    token: str
    challenge: Optional[str]
    type: str


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hoge'}


@app.post('/slack_event_callback')
def slack_event_callback(request: dict):
    if 'type' not in request:
        raise HTTPException(
            status_code=400,
            detail='Invalid request_type'
        )
    request_type = request['type']
    if request_type == 'url_verification':
        if 'challenge' in request:
            return request['challenge']
        else:
            raise HTTPException(
                status_code=400,
                detail="challenge code must be included."
            )

    if request_type == 'message':
        event = MessageEvent.parse_obj(request.get('event'))

    return {'message': event.text}
