import datetime
import json
import re
import urllib2
import sys

if sys.version_info < (3, 0):
    import urllib2
else:
    import urllib.request

import deform
import colander
from beaker.cache import (cache_region,
                          cache_regions)

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from friendfinder.strava import Athlete

cache_regions.update({
    'short_term':{
        'expire':3600,
        'type':'memory',
        'key_length':80,
    },
})

@cache_region('short_term', 'friends')
def get_friends(id):
    st = Athlete(id)
    start_date = datetime.datetime.today()-datetime.timedelta(days=30)

    segment_ids = []
    rider_ids = {}

    try:
        for ride in st.rides(start_date=start_date):
            for segment in ride.segments:
                if not segment.detail.id in segment_ids:
                    segment_ids.append(segment.detail.id)
                    try:
                        """
Strava doesn't honor startDate when best=true
                        """
                        req = urllib2.Request( \
                            'http://app.strava.com/api/v1/segments/%d/efforts?' \
                            'startDate=%s&best=true' % (segment.detail.id, \
                            start_date.isoformat()))
                        rsp = urllib2.urlopen(req)
                    except urllib2.HTTPError as e:
                        raise APIError("%s: request failed: %s" % (url, e))
                    segment_url = \
                        'http://app.strava.com/api/v1/segments/%d/efforts?' \
                        'startDate=%s&best=true' % (segment.detail.id, \
                        start_date.isoformat())
                    if sys.version_info < (3, 0):
                        try:
                            req = urllib2.Request(segment_url)
                            rsp = urllib2.urlopen(req)
                        except urllib2.HTTPError as e:
                            raise APIError("%s: request failed: %s" % (url, e))
                    else:
                        try:
                            rsp = urllib.request.urlopen(segment_url)
                        except urllib.error.HTTPError as e:
                            raise APIError("%s: request failed: %s" % (url, e))
                    txt = rsp.read().decode('utf-8')
                    try:
                        json_result = json.loads(txt)
                    except (ValueError, KeyError) as e:
                        raise APIError("%s: parsing response failed: %s" % (url, e))
                    for effort in json_result['efforts']:
                        effort_time = datetime.datetime.strptime( \
                            effort['startDate'], '%Y-%m-%dT%H:%M:%SZ')
                        if effort_time > start_date:
                            if effort['athlete']['id'] not in rider_ids:
                                rider_ids[effort['athlete']['id']] = \
                                    effort['athlete']['name']
        del rider_ids[int(id)]
    except:
        pass
    return(rider_ids)

@colander.deferred
def deferred_csrf_token(node, kw):
    """
    generate the value for the csrf token to be inserted into the form

    .. codeblock:: python

    # define form schema
    from apex.ext.deform import deferred_csrf_token

    class SubmitNewsSchema(MappingSchema):
        csrf_token = colander.SchemaNode(
        colander.String(),
            widget = deform.widget.HiddenWidget(),
            default = deferred_csrf_token,
        )

    # in your view, bind the token to the schema
    schema = SubmitNewsSchema(validator=SubmitNewsValidator).bind(csrf_token=request.session.get_csrf_token())

    """
    csrf_token = kw.get('csrf_token')
    return csrf_token

url_re = re.compile('^http://.*/(\d+)$')

def url_validator(url):
    try:
        valid = url_re.match(url)
        return True
    except Exception as message:
        return unicode(message)

class URLSchema(colander.Schema):
    csrf_token = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.HiddenWidget(),
        default = deferred_csrf_token,
    )
    strava_url = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.TextInputWidget(css_class = 'span7'),
        title = 'Strava Profile URL',
        validator = colander.Function(url_validator),
    )

@view_config(route_name='home', renderer='index.mako')
def index(request):
    schema = URLSchema().bind(csrf_token=request.session.get_csrf_token())
    form = deform.Form(schema, buttons=('Find Local Riders',))
    if request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form':e.render()}
        strava_id = url_re.search(appstruct['strava_url']).group(1)
        return HTTPFound(location='/friends/%s' % strava_id)
    return {'form':form.render()}

@view_config(route_name='friends', renderer='friends.mako')
def friends(request):
    return {'id':request.matchdict['id']}

@view_config(route_name='strava_id', renderer='json')
def strava_id(request):
    return {'riders':get_friends(request.matchdict['id'])}
