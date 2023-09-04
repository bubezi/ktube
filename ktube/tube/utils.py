from django.utils import timezone
    
def period(time_upload):
    """Takes in a datetime object and calculates the difference the time 
    difference between now and the datetime object in all units 
    (From Seconds to Years) AND returns the difference 
    of the smallest unit of time.

    Args:
        time_upload (datetime): a datetime object

    Returns:
        str: the difference of the smallest unit of time
    """
    
    now = timezone.now()
    seconds = now.second - time_upload.second
    minutes = now.minute - time_upload.minute
    hours = now.hour - time_upload.hour 
    days = now.day - time_upload.day
    months = now.month - time_upload.month
    years = now.year - time_upload.year
    
    if years==0:
        if months==0:
            if days==0:
                if hours==0:
                    if minutes==0:
                        if not seconds == 1:
                            return f'{seconds} seconds ago'
                        else:
                            return f'{seconds} second ago'
                    else:
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
        

def view_valid(view, INVALID_MINUTES=30):
    """Returns True if the view is more than INVALID_MINUTES

    Args:
        view (tube.models.VideoView): An object of the model VideoView in the app tube
        INVALID_MINUTES (int, optional): The number of minutes in which a view is invalid. Defaults to 30.

    Returns:
        Bool: Returns a wether the view is valid or not
    """
    then = view.viewed_on
    now = timezone.now()
    
    diff = now - then
    if diff.total_seconds() > (INVALID_MINUTES * 60):
        return True
    else:
        return False
    