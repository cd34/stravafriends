#!/var/www/strava32/bin/python

import os
import site
site.addsitedir('/var/www/strava32/lib/python3.2/site-packages')
from pyramid.paster import get_app
application = get_app(
    '/var/www/strava32/friendfinder/production.ini', 'main')
