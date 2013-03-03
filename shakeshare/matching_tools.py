from datetime import timedelta 
from shakeshare.models import Shake
from django.db import transaction
'''
from math import cos
from math import acos
from math import sin
'''

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
    # filter non-near shakes
    '''
    for matching_shake in matching_shakes:
        if isTwoShakeNearEachOther(matching_shake, shake) == False:
            matching_shakes.remove(matching_shake)
    '''
    return matching_shakes

'''
def isTwoShakeNearEachOther(shake1, shake2):
    lat1 = shake1.latitude
    lat2 = shake2.latitude
    log1 = shake1.logitude
    log2 = shake2.logitude
    acy1 = shake1.accuracy
    acy2 = shake2.accuracy
    R = 6367449 # in meters
    distance = math.acos(math.sin(lat1)*math.sin(lat2) +
            math.cos(lat1)*math.cos(lat2) *
            math.cos(lon2-lon1)) * R;
    if distance < DISTANCE_THRESHHOLD:
        return true
    else:
        return false
'''
