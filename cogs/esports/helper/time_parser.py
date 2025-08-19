import re
from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz

# Define the timezone for India Standard Time
IST = pytz.timezone("Asia/Kolkata")

def parse_time(time_str: str) -> datetime:
    """
    Parses a flexible time string and returns a future, timezone-aware datetime object in UTC.
    
    Handles relative time (e.g., '2h', '30m'), 12-hour format ('5pm', '4:00am'), 
    and 24-hour format ('13:00').
    """
    now_utc = datetime.now(pytz.utc)
    now_ist = now_utc.astimezone(IST)
    
    # --- 1. Check for relative time (e.g., 1d, 2h, 30m) ---
    relative_match = re.match(r"(\d+)\s*(d|h|m)$", time_str.lower())
    if relative_match:
        value = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        if unit == 'd':
            return now_utc + timedelta(days=value)
        elif unit == 'h':
            return now_utc + timedelta(hours=value)
        elif unit == 'm':
            return now_utc + timedelta(minutes=value)

    # --- 2. Parse absolute time (e.g., 5pm, 13:00, 4:00am) ---
    try:
        # The 'fuzzy=True' helps parse strings like "5pm" correctly
        parsed_time = parse(time_str, fuzzy=True)
        
        # Combine the parsed time with today's date in IST
        scrim_time_ist = now_ist.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0
        )
        
        # If the calculated time is in the past for today, schedule it for tomorrow
        if scrim_time_ist < now_ist:
            scrim_time_ist += timedelta(days=1)
            
        # Convert the final IST time back to UTC for storage
        return scrim_time_ist.astimezone(pytz.utc)

    except ValueError:
        raise ValueError("Invalid time format. Use '2h', '5pm', '13:00', etc.")
