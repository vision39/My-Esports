import re
from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz

# Define the timezone for India Standard Time
IST = pytz.timezone("Asia/Kolkata")

def parse_time(time_str: str) -> datetime:
    """
    Parses a flexible time string and returns a future, naive datetime object representing IST.
    
    Handles relative time (e.g., '2h', '30m'), 12-hour format ('5pm', '4:00am'), 
    and 24-hour format ('13:00').
    """
    now_ist = datetime.now(IST)
    
    # --- 1. Check for relative time (e.g., 1d, 2h, 30m) ---
    relative_match = re.match(r"(\d+)\s*(d|h|m)$", time_str.lower())
    if relative_match:
        value = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        if unit == 'd':
            # Return a naive datetime object
            return (now_ist + timedelta(days=value)).replace(tzinfo=None)
        elif unit == 'h':
            return (now_ist + timedelta(hours=value)).replace(tzinfo=None)
        elif unit == 'm':
            return (now_ist + timedelta(minutes=value)).replace(tzinfo=None)

    # --- 2. Parse absolute time (e.g., 5pm, 13:00, 4:00am) ---
    try:
        parsed_time = parse(time_str, fuzzy=True)
        
        scrim_time_ist = now_ist.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0
        )
        
        # If the calculated time is in the past for today, schedule it for tomorrow
        if scrim_time_ist < now_ist:
            scrim_time_ist += timedelta(days=1)
            
        # Return the final IST time as a naive datetime object
        return scrim_time_ist.replace(tzinfo=None)

    except ValueError:
        raise ValueError("Invalid time format. Use '2h', '5pm', '13:00', etc.")
