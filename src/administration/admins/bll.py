import calendar
import datetime

from src.administration.admins.models import ShiftDay, Shift


def date_range(shift_id, start, end, repeat_policy, *args):
    delta = end - start
    days = []
    shift = Shift.objects.get(pk=shift_id)
    shift.week_days = ""

    # CHECK FOR WEEK DAYS - REPEAT
    if repeat_policy == 'w':

        # GETTING INDEXES
        args = list(args[0])
        days_in_count = []
        count = 0

        for x in args:
            if x == 'on':
                days_in_count.append(count)
            count += 1

        for i in range(delta.days + 1):

            _date = start + datetime.timedelta(days=i)
            if _date.weekday() in days_in_count:
                days.append(_date)

        shift.week_days = ''.join([str(elem) for elem in days_in_count])

    # IF NOT WEEK NEITHER DATES
    elif repeat_policy == 'd':
        days = list(args[0][0])
    else:
        days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]

    shift.save()
    return days


def shifts_create_update_logic(shift, is_create=True, *args, **kwargs):
    dates = date_range(shift.id, shift.start_date, shift.end_date, shift.repeat_policy, args)

    if not is_create:
        ShiftDay.objects.filter(shift=shift).delete()
        [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]
    else:
        [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]


def shifts_create_update(shift, post, is_create=True):
    # if shift policy is regular
    if shift.repeat_policy == 'r':
        shifts_create_update_logic(shift, is_create)

    # if shift policy is week
    elif shift.repeat_policy == 'w':
        shifts_create_update_logic(
            shift, is_create,
            post.get('monday'), post.get('tuesday'), post.get('wednesday'), post.get('thursday'), post.get('friday'),
            post.get('saturday'), post.get('sunday')
        )

    # if shift policy is dates
    elif shift.repeat_policy == 'd':
        date_index_names = []
        date_index_values = []

        [date_index_names.append(key_name) if "car" in key_name else None for key_name in post]
        [date_index_values.append(post[f'{name}']) for name in date_index_names]
        shifts_create_update_logic(shift, is_create, date_index_values)
