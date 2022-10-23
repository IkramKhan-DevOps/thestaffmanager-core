from datetime import datetime, date

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.administration.admins.models import Shift, ShiftDay


class ChangeTimesAPI(APIView):

    def post(self, request, pk, *args, **kwargs):
        context = {'message': 'Something went wrong'}

        # CHECK SHIFT AVAILABILITY
        shift = Shift.objects.filter(pk=pk)
        if not shift:
            context['message'] = f"Shift with ID:{pk} doesn't exists"
            return Response(status=HTTP_404_NOT_FOUND, data=context)

        # CHECK INPUTS
        old_time_start = request.POST.get('old_time_start')
        old_time_end = request.POST.get('old_time_end')
        new_time_start = request.POST.get('new_time_start')
        new_time_end = request.POST.get('new_time_end')
        direction = request.POST.get('direction')

        if not all([old_time_start, old_time_end, new_time_start, new_time_end, direction]):
            context['message'] = f"Missing inputs in API Call"
            return Response(status=HTTP_400_BAD_REQUEST, data=context)

        # CONVERT TO PYTHON DATETIME
        old_time_start = datetime.strptime(old_time_end, "%a, %d %b %Y %H:%M:%S %Z")
        old_time_end = datetime.strptime(old_time_end, "%a, %d %b %Y %H:%M:%S %Z")
        new_time_start = datetime.strptime(new_time_start, "%a, %d %b %Y %H:%M:%S %Z")
        new_time_end = datetime.strptime(new_time_end, "%a, %d %b %Y %H:%M:%S %Z")
        shift = shift.first()

        if direction == "time":
            print("TIME")
            print("----")

            print("OLD START TIME: ", shift.start_time)
            print("OLD END   TIME: ", shift.end_time)

            shift.start_time = new_time_start.time()
            shift.end_time = new_time_end.time()
            # shift.save()

            print("NEW START TIME: ", shift.start_time)
            print("NEW END   TIME: ", shift.end_time)

        elif direction == "date":
            print("DATE")
            print("----")

            previous_date = old_time_end.date()
            new_date = new_time_end.date()
            old_time = old_time_end.time()
            new_time = new_time_end.time()

            if previous_date != new_date:
                print("DATE CHANGE")
                print("----")

                shift_day = ShiftDay.objects.filter(shift=shift, shift_date=previous_date)
                if shift:
                    shift_day = shift_day[0]
                    print("FROM: ", shift_day.shift_date)

                    shift_day.shift_date = new_date
                    # shift_day.save()

                    print("TO  : ", shift_day.shift_date)

            if old_time != new_time:
                print("TIME CHANGE")
                print("----")

                print("OLD START TIME: ", shift.start_time)
                print("OLD END   TIME: ", shift.end_time)

                shift.start_time = new_time_start.time()
                shift.end_time = new_time_end.time()
                # shift.save()

                print("NEW START TIME: ", shift.start_time)
                print("NEW END   TIME: ", shift.end_time)

        context['message'] = f"Times changed successfully"
        return Response(status=HTTP_200_OK, data=context)

