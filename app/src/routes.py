from .event_analyzer import EventAnalyzer
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
    date: Optional[str] = Query(None, alias="yyyy-mm-dd", description ="Filter events by date"),
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
    try:
        events_data = EventFileManager.read_events_from_file()

        for event in events_data:
            if event["id"] == event_id:
                return event

        raise Exception("Event not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    try:
        events_data = EventFileManager.read_events_from_file()
        
        for exist_event in events_data:
            if exist_event["id"] == event.id:
                raise Exception("Event ID already exists")

        event_dict = json.loads(json.dumps(event, default=lambda o: o.__dict__))
        events_data.append(event_dict)
        
        EventFileManager.write_events_to_file(events_data)

        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    try:
        events_data = EventFileManager.read_events_from_file()
        for exist_event in events_data:
            if exist_event["id"] == event_id:
                event_dict = json.loads(json.dumps(event, default=lambda o: o.__dict__))
                # print(type(json.dumps(event, default=lambda o: o.__dict__)))
                # type string
                exist_event.update(event_dict)

                EventFileManager.write_events_to_file(events_data)
                return exist_event

        raise Exception("Event not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
    
        

@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    try:
        events_data = EventFileManager.read_events_from_file()
        for event in events_data:
            if event["id"] == event_id:
                events_data.remove(event)
                EventFileManager.write_events_to_file(events_data)
                return {"message": "Events deleted successfully"}
        
        raise Exception("Event not found")
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    try:
        events_data = EventFileManager.read_events_from_file() #return dict
        events = [Event(**event_data) for event_data in events_data] #turn list dict to list obj E
        joiners_multi = EventAnalyzer.get_joiner_multiple_meetings_method(events)

        if not joiners_multi:
            return {"message": "No joiners attending at least 2 meetings"}
        return joiners_multi
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
