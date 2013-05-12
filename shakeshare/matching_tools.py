from datetime import timedelta 
from shakeshare.models import Shake
from django.db import transaction


import math
import logging

logger = logging.getLogger(__name__)

@transaction.commit_manually
def flush_transaction():
    transaction.commit()

'''
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

def find_matching_shakes(shake): 
    # need to flush transaction to get the latest data in database
    flush_transaction()
    #logger.debug("system is finding matching shakes for shake id " + unicode(shake.id) + " from " + unicode(Shake.objects.count()) + " existing shake objects")
    shake_time = shake.time
    delta = timedelta(seconds=5)
    shake_time_lowerbound = shake_time - delta
    shake_time_upperbound = shake_time + delta
    matching_shakes = list(Shake.objects.filter(
            time__range=(shake_time_lowerbound, shake_time_upperbound)))
    '''
    # filter non-near shakes
    for matching_shake in matching_shakes:
        if areTwoShakesNearEachOther(matching_shake, shake) == False:
            matching_shakes.remove(matching_shake)
    '''
    # if just find itself, this is not a sucessful matching
    if len(matching_shakes) == 1 and matching_shakes[0] == shake:
        matching_shakes = []
    return matching_shakes

'''
def areTwoShakesNearEachOther(shake1, shake2):
    DISTANCE_THRESHHOLD = 5000 # in meters
    lat1 = shake1.latitude
    lat2 = shake2.latitude
    lon1 = shake1.longitude
    lon2 = shake2.longitude
    acy1 = shake1.accuracy
    acy2 = shake2.accuracy
    R = 6367449 # in meters
    distance = math.acos(math.sin(lat1)*math.sin(lat2) +
            math.cos(lat1)*math.cos(lat2) *
            math.cos(lon2-lon1)) * R;
    logger.debug("distance: " + unicode(distance))
    if distance < DISTANCE_THRESHHOLD:
        return True
    else:
        return False
'''
