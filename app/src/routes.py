from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .models import Event
import json
from .file_storage import EventFileManager, Event
router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events_data = EventFileManager.read_events_from_file()
    return events_data
    


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(
    date: Optional[str] = Query(None, description ="Filter events by date"),
    organizer: Optional[str] = Query(None, description="Filter events by organizer's name"),
    status: Optional[str] = Query(None, description="Filter events by status"),
    event_type: Optional[str] = Query(None, description="Filter events by type")
):
    events_data = EventFileManager.read_events_from_file()
    filtered_events = []

    for event in events_data:
        if (date is None or event["date"] == date) and \
        (organizer is None or event["organizer"]["name"] == organizer ) and \
        (status is None or event["status"] == status) and \
        (event_type is None or event["type"] == event_type):
            filtered_events.append(event)
    
    return filtered_events

@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    pass


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    pass


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    pass


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    pass


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
