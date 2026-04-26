from datetime import timedelta

SELECTABLE_TIME_FRAMES = {
    "1 month": timedelta(days=30),
    "1 week":  timedelta(weeks=1),
    "1 day":   timedelta(days=1),
    "1 hour":  timedelta(hours=1),
}