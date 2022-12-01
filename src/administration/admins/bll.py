import calendar
import datetime

from src.administration.admins.models import ShiftDay, Shift


# GET DATES: between (start - end) according to policy.
def date_range(shift, start, end, repeat_policy, *args):
    """
    :param shift:
    :param start: form where to start dates
    :param end: from where to end dates
    :param repeat_policy: how dates are captured
    :param args: extra info (selected dates - week dates etc)
    :return:
    """

    delta = end - start
    days = []
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
        [days.append(datetime.datetime.strptime(x, '%Y-%m-%d')) for x in args[0][0]]
    else:
        days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]

    shift.save()
    return days


# STEP3: if request for update
def shifts_update_in(dates, shift, previous_shift, refresh):
    if shift.start_date == previous_shift.start_date and shift.end_date == previous_shift.end_date and \
            shift.repeat_policy == previous_shift.repeat_policy and shift.week_days == previous_shift.week_days:
        if refresh:
            print("Changes required ... ")
            ShiftDay.objects.filter(shift=shift).delete()
            [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]
        else:
            print("Not changes detected")
    else:
        print("changes required")
        ShiftDay.objects.filter(shift=shift).delete()
        for _date in dates:
            print(_date)
            ShiftDay.objects.create(shift_date=_date, shift=shift)


# STEP3: if request for create
def shift_create_in(dates, shift):
    [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]


# STEP2: get dates and redirect according to request type.
def shifts_create_update_logic(shift, is_create, previous_shift, refresh, *args):
    dates = date_range(shift, shift.start_date, shift.end_date, shift.repeat_policy, args)
    shifts_update_in(dates, shift, previous_shift, refresh) if not is_create else shift_create_in(dates, shift)


# STEP1: input request with (create/update) - (policy-type)
def shifts_create_update(shift, post, is_create=True, refresh=False, previous_shift=None):
    # if shift policy is regular
    if shift.repeat_policy == 'r':
        shifts_create_update_logic(shift, is_create, previous_shift, refresh)

    # if shift policy is week
    elif shift.repeat_policy == 'w':
        shifts_create_update_logic(
            shift, is_create, previous_shift, refresh,
            post.get('monday'), post.get('tuesday'), post.get('wednesday'), post.get('thursday'),
            post.get('friday'),
            post.get('saturday'), post.get('sunday')
        )

    # if shift policy is dates
    elif shift.repeat_policy == 'd':
        date_index_names = []
        date_index_values = []

        # get keys first then names
        [date_index_names.append(key) if "car" in key else None for key, name in post.items()]
        [date_index_values.append(post[f'{name}']) for name in date_index_names]

        # if difference in length
        if len(date_index_values) != ShiftDay.objects.filter(shift=shift).count():
            refresh = True

        shifts_create_update_logic(shift, is_create, previous_shift, refresh, date_index_values)


def get_shift_days_dict(shift):
    """
    :param shift: model object:
    :return:
    """
    days = [0, 1, 2, 3, 4, 5, 6]
    context = {"days": []}
    if shift.repeat_policy == 'w':
        week_list = shift.get_week_shifts_status()
        for day in days:
            pass
        context['days'].append({'name': 'day', 'on': True})
