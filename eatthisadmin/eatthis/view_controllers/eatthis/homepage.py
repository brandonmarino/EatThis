from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from copy import deepcopy

import requests
import random
import json

#
# Load the context for the page and return the http response for the page
#
def load_home_page(request):
    context = {
        "restaurants": [],
        "selected_restaurant": {}
    }
    if request.GET.get('getplaces'):
        # get local places with the provided url params
        local_places = get_local_places(request)
        if local_places is not None:
            context = local_places
        if len(context['restaurants']) > 0:
            context['selected_restaurant'] = random.choice(context['restaurants'])

    # load the dietry restriction context with data from the current route
    context['dietary_restrictions'] = get_dietary_restrictions(request)
    template = loader.get_template('eatthis/homepage.html')
    return HttpResponse(template.render(context, request))
#
# Load all dietary restrictions and set which ones were selected by the user
#
def get_dietary_restrictions(request):
    selected_dietary_restrictions = str(request.GET.getlist('dietary_restrictions'))
    # return our list of dietary restrictions and if they will be selected due to the current path
    all_dietary_restrictions = deepcopy(settings.DIETARY_RESTRICTIONS)
    for restriction in all_dietary_restrictions:
        restriction['selected'] = (restriction['value'] in selected_dietary_restrictions)
    return all_dietary_restrictions

# Get any additional terms we would like to add to the restaurant filter 
# These will assist fourquare and give the user more options for places to eat
def get_additional_terms_for_search(selected_dietary_restrictions):
    all_dietary_restrictions = deepcopy(settings.DIETARY_RESTRICTIONS)
    query_additional_terms = ''
    for restriction in all_dietary_restrictions:
        if hasattr(restriction, 'additional-terms') and restriction['value'] in selected_dietary_restrictions:
            query_additional_terms += restriction['additional-terms']
    return query_additional_terms
#
# Query Forquare for local restaurants meeting the given criteria.
# Return this list to be consumed as context for the page
#
def get_local_places(request):
    # these need to gtfo of here before this goes up on github
    client_id = settings.FOURSQUARE_KEYS['client_id']
    client_secret = settings.FOURSQUARE_KEYS['client_secret']
    api_version = settings.FOURSQUARE_KEYS['api_version']

    # get gelocation from the given url
    geo_location = request.GET.get('geo_location')
    # get the range from the form
    range = request.GET.get('range')
    # the radius from the user that the app will accept. These should change to a dropdown for the user
    radius = str(int(range)*100)

    # strip off the array brackets
    geo_location = geo_location.strip('[]')
    # get the dietary restrictions of this user from the url
    dietary_restrictions = str(request.GET.getlist('dietary_restrictions'))
    # prepare dietary restrictions for the url by stripping off unneccessary characters
    dietary_restrictions = dietary_restrictions.strip('[]').replace("u'", "").replace("'", "")

    # adding keywords based on restrictions which make the query more robust
    dietary_metadata = get_additional_terms_for_search(dietary_restrictions)

    dietary_restrictions += ' ' + dietary_metadata + ' '

    # build the url to query fourspuare for near by restaurants
    url = 'https://api.foursquare.com/v2/venues/explore?client_id=' + client_id + '&client_secret=' + client_secret + '&ll=' + geo_location + '&query=restaurant ' + dietary_restrictions + '&v=' + api_version + '&radius=' + radius + '&openNow=1'
    response = requests.get(url)
    
    # get the recommendations from the response
    if response.json()['response'] and response.json()['response']['groups']:
        restaurant_items = response.json()['response']['groups'][0]['items']

        # strip of a bunch of unneccessary information that we will not be using in this app
        restaurant_venues = []
        for current_restaurant in restaurant_items:
            restaurant_venues.append(current_restaurant['venue'])
        
        return { 'restaurants': restaurant_venues }
