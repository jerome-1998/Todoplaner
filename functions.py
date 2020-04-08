from flask import render_template, request
from functools import wraps

# stelle alle Sortierfilter ein und gib das Dictionary weiter
def sortable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = func()
        #prüfen ob funktion ein Dictionary ist, wenn nicht erstelle eines
        if not isinstance(ctx, dict):
            ctx= dict(query = ctx)
        sort_direction = request.args.get('sort_dir')
        if sort_direction:
            ctx['sort_direction'] = sort_direction
        return ctx 
    return wrapper

# stelle Filter ein und reiche das Dictionary weiter
def filterable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = func()
        # prüfe ob empfangene Funktion bereits ein Dictionary ist, wenn nicht erstelle eines
        if not isinstance(ctx, dict):
            ctx= dict(query = ctx)
        filter_by = request.args.get('filter_art')
        if filter_by:
            ctx['filter_by'] = filter_by
        return ctx
    return wrapper

