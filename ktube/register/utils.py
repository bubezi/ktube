from django.utils import timezone
import json


def check_errors(form):
    """Checks a form's errors and returns """
    try:
        errors = 'System error: Bug report sent to developers. If it persists for longer than a day please contact customer care.'
        errorss = list(json.loads(form.errors.as_json()).values())
        if errorss:
            errors = list((list(json.loads(form.errors.as_json()).values())[0][0]).values())[0]
            if len(errorss) > 1:
                errors2 = list((list(json.loads(form.errors.as_json()).values())[1][0]).values())[0]
                errors = errors + " & also " + errors2
        return errors
    except:
        return 'System error: Bug report sent to developers. If it persists for longer than a day please contact customer care.'
    
    
def period(time_upload):
    """Takes in a time object and calculates the time in the smallest units (From minutes to Years) AND returns the difference 
    of the smallest unit of time."""
    now = timezone.now()
    minutes = now.minute -time_upload.minute
    hours = now.hour - time_upload.hour 
    days = now.day - time_upload.day
    months = now.month - time_upload.month
    years = now.year - time_upload.year
    if now.year==time_upload.year:
        if now.month==time_upload.month:
            if now.day==time_upload.day:
                if now.hour==time_upload.hour:
                    if not minutes == 1:
                        return f'{minutes} minutes ago'
                    else:
                        return f'{minutes} minute ago'
                else:
                    if not hours == 1:
                        return f'{hours} hours ago'
                    else:
                        return f'{hours} hour ago'
            else:
                if not days == 1:
                    return f'{days} days ago'
                else:
                    return f'{days} day ago'
        else:
            if not months == 1:
                return f'{months} months ago'
            else:
                return f'{months} month ago'
    else:
        if not years == 1:
            return f'{years} years ago'
        else:
            return f'{years} year ago'