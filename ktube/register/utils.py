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
    
