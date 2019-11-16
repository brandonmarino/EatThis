from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

import requests
import random
import json

def load_home_page(request):
    context = {}
    if(request.GET.get('getplaces')):
        # get local places with the provided url params
        context = get_local_places(request)
        # context['selected_restaurant'] = random.choice(context['restaurants'])
    # load the dietry restriction context with data from the current route
    # context['dietary_restrictions'] = get_dietary_restrictions(request)
    template = loader.get_template('bitequick/homepage.html')
    return HttpResponse(template.render(context, request))

def get_dietary_restrictions(request):
    dietary_restrictions = str(request.GET.getlist('dietary_restrictions'))
    # return our list of dietary restrictions and if they will be selected due to the current path
    return [
        {
            'name': 'Pescatarian',
            'value': 'pescatarian',
            'selected': ('pescatarian' in dietary_restrictions)
        },
        {
            'name': 'Vegetarian (Lacto-ovo)',
            'value': 'lacto-ovo-vegetarian',
            'selected': ('lacto-ovo-vegetarian' in dietary_restrictions)
        },
        {
            'name': 'Vegan',
            'value': 'vegan',
            'selected': ('vegan' in dietary_restrictions)
        },
        {
            'name': 'gluten free',
            'value': 'gluten-free',
            'selected': ('gluten-free' in dietary_restrictions)
        }
    ]
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
    dietary_restrictions = dietary_restrictions.strip('[]').replace("u'", "")

    # adding keywords based on restrictions which make the query more robust
    dietary_metadata = ''

    if ('pescatarian' in dietary_restrictions):
        dietary_metadata += ' fish '

    if ('gluten' in dietary_restrictions):
        dietary_metadata += ' celiac '

    # build the url to query fourspuare for near by restaurants
    url = 'https://api.foursquare.com/v2/venues/explore?client_id=' + client_id + '&client_secret=' + client_secret + '&ll=' + geo_location + '&query=restaurant ' + dietary_restrictions + '&v=' + api_version + '&radius=' + radius + '&openNow=1'
    r = requests.get(url)

    # get the recommendations from the response
    if (r.json()['response'] and r.json()['response']['groups']):
        restaurant_items = r.json()['response']['groups'][0]['items']

        # strip of a bunch of unneccessary information that we will not be using in this app
        restaurant_venues = []
        for current_restaurant in restaurant_items:
            print(current_restaurant['venue'])
            restaurant_venues.append(current_restaurant['venue'])
        
        return { 'restaurants': restaurant_venues }
