# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from view_controllers.bitequick.homepage import load_home_page

def index(request):
    return load_home_page(request)