#!/var/www/strava/bin/python

import os
import site
site.addsitedir('/var/www/strava/lib/python2.7/site-packages')
from pyramid.paster import get_app
application = get_app(
    '/var/www/strava/friendfinder/production.ini', 'main')
