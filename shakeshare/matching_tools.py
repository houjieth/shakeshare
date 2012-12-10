from datetime import timedelta 
from shakeshare.models import Shake
from django.db import transaction

@transaction.commit_manually
def flush_transaction():
    transaction.commit()

def find_matching_shakes_by_time(shake): 
    # need to flush transaction to get the latest data in database
    flush_transaction()
    print "finding matching shakes for shake id " + unicode(shake.id) + " Shake objects count: " + unicode(Shake.objects.count())
    shake_time = shake.time
    delta = timedelta(seconds=4)
    shake_time_lowerbound = shake_time - delta
    shake_time_upperbound = shake_time + delta
    matching_shakes = list(Shake.objects.filter(
            time__range=(shake_time_lowerbound, shake_time_upperbound)))
    # if just find itself, this is not a sucessful matching
    if len(matching_shakes) == 1 and matching_shakes[0] == shake:
        matching_shakes = []
    return matching_shakes

'''
def find_matching_shakes_by_time_and_geolocation(shake)
    matching_shakes = find_matching_shakes_by_time(shake)
    if len(matching_shakes) == 0:
        return matching_shakes
    for matching_shake in matching_shakes:
        if calc_distance(shake, matching_shake) > 10:
            matching_shakes
            '''
