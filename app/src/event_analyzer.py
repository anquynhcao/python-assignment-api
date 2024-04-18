from typing import List
from .models import Joiner, Event

class EventAnalyzer:
    def get_joiner_multiple_meetings_method(events: List[Event]) -> List[Joiner]:
        joiner_meeting_count = {}
        joiner_details = {}
        for event in events:
             if event.joiners:
                for joiner in event.joiners:
                    print(joiner)
                    if joiner.email in joiner_meeting_count:
                        joiner_meeting_count[joiner.email] += 1
                    else:
                        joiner_meeting_count[joiner.email] = 1
                        joiner_details[joiner.email] = joiner

        joiners_multiple_meeting = []
        for joiner in joiner_meeting_count:
            if joiner_meeting_count[joiner] >=2:
                
                joiners_multiple_meeting.append(joiner_details[joiner])
                
        return joiners_multiple_meeting
    