import calendar
import datetime

from src.administration.admins.models import ShiftDay


def date_range(start, end):
    """
    :param start:
    :param end:
    :return dates in range:

    :desc check this first if it is in month, year and daily routine vise
    """
    delta = end - start

    # TODO:REQUIREMENT: add checks here month repeat - weekly repeat
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


def shifts_create_update_logic(shift, is_create=True):
    """
    :param shift:
    :param is_create:
    :return None:

    ":desc add new one's and delete previous ones"

    """

    dates = date_range(shift.start_date, shift.end_date)

    # TODO:ALERT: this deletes all previous records and adds new ones --
    #  this logic is wrong if data is long and lengthy
    if not is_create:
        ShiftDay.objects.filter(shift=shift).delete()
        [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]
    else:
        [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]