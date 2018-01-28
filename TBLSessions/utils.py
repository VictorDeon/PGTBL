from django.utils import timezone
from datetime import timedelta


def get_datetimes(session):
    """
    Get iRAT and gRAT datetimes.
    """


    irat_datetime = (
        timezone.localtime(session.irat_datetime) -
        timedelta(minutes=session.irat_duration)
    )

    grat_datetime = (
        timezone.localtime(session.grat_datetime) -
        timedelta(minutes=session.grat_duration)
    )

    return irat_datetime, grat_datetime
