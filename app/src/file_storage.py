from .models import Event
import json



class EventFileManager:
    FILE_PATH = "event.json"

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                events_data = json.load(file)
                # print(type(events_data[0]))
                # type dict
                return events_data
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error reading events file: {e}")
            return []
        
    @classmethod
    def write_events_to_file(cls, events):
        try:
            with open(cls.FILE_PATH, "w") as file:
                json.dump(events, file, indent=4)

        except Exception as e:
            print(f"Error writing events file: {e}")
        
    