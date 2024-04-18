from typing import List
from .models import Joiner, Event

class EventAnalyzer:
    def get_joiner_multiple_meetings_method(events: List[Event]) -> List[Joiner]:
        joiner_meeting_count = {}
        for event in events:
            for joiner in events.joiners:
                if joiner.email in joiner_meeting_count:
                    joiner_meeting_count[joiner.email] += 1
                else:
                    joiner_meeting_count[joiner.email] = 1

        joiners_multiple_meeting = [Joiner(name=joiner_name,email=joiner_email,country=joiner_country)
                                    for joiner_email, meeting_attend in joiner_meeting_count.items()
                                    if meeting_attend > 1
                                    for joiner_name, joiner_country in [(event.joiner.name, event.joiner.country) 
                                    for event in events if event.joiner.email == joiner_email]]
        return joiners_multiple_meetings
    