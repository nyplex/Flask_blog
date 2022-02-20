from datetime import datetime

def format_post_date(postDate):
        then = postDate
        now  = datetime.now() 
        duration = now - then
        duration_in_s = duration.total_seconds() 
        
        years = divmod(duration_in_s, 31536000)[0]    # Seconds in a year=365*24*60*60 = 31536000.
        days  = divmod(duration_in_s, 86400)[0]       # Seconds in a day = 86400
        hours = divmod(duration_in_s, 3600)[0]
        minutes = divmod(duration_in_s, 60)[0] 
        if years > 0:
            return str(int(years)) + "y"
        if days > 0:
            return str(int(days)) + "d"
        if hours > 0:
            return str(int(hours)) + "h"
        if minutes > 0:
            return str(int(minutes)) + "m"
        if duration_in_s > 30:
            return str(int(duration_in_s)) + "s"
        if duration_in_s > 0:
            return "now"
        return "now"