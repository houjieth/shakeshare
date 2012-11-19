from datetime import timedelta 
from shakeshare.models import Shake

def find_matching_shakes_by_time(shake): 
    shake_time = shake.time
    delta = timedelta(seconds=2)
    shake_time_lowerbound = shake_time - delta
    shake_time_upperbound = shake_time + delta
    matching_shakes = list(Shake.objects.filter(
            time__range=(shake_time_lowerbound, shake_time_upperbound)))
    # remove itself
    for s in matching_shakes:
        if s.session_id == shake.session_id:
            matching_shakes.remove(s)
    return matching_shakes
