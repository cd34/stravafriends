Quick Pyramid app that uses the Strava API (Version 1) to find riders that
have ridden segments that you've ridden in the last 30 days. The app was
written originally to test Python 2.7/3.2 compatibility in a single application.

As of June 30, 2013, Strava appears to be shutting down API1/API2 and
requiring all apps transition to API3 which requires a key which I've not
been granted.

deploy32.wsgi is the wsgi script for Python 3.2
deploy.wsgi is the wsgh script for Python 2.6/2.7
