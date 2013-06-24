<%inherit file="template.mako"/>

<%def name="title()">
</%def>

<%def name="body()">
<br/>
<div class="hero-unit">
<h2>What is this site?</h2>
<p>This site allows you to put your Strava url into the form and it will
look for other riders that have ridden segments you have ridden in the last
30 days.</p>
<p>You'll be presented with a list of results, click their names, view their profiles and follow them.</p>
</div>
${form|n}
<p>Go to <a href="http://strava.com/" target="_new">Strava.com</a>, click on 
your profile, then cut and paste the URL for your profile into the field above.</p>
<h4>Note: this is not endorsed by Strava. It makes use of their API. No 
password or authentication information is needed. Only your profile URL is
used to query the API.</h4>
<script type="text/javascript">
var a=["https://apis.google.com/js/plusone.js","http://platform.twitter.com/widgets.js","http://connect.facebook.net/en_US/all.js#appId=238646832821223&xfbml=1"];for(script_index in a){var b=document.createElement("script");b.type="text/javascript";b.async=!0;b.src=a[script_index];var c=document.getElementsByTagName("script")[0];c.parentNode.insertBefore(b,c)};
</script>
<br/>
<div class="row">
<div style="float:left;">
<g:plusone href="http://stravafriends.cd34.com/"></g:plusone>
</div><div style="float:left;">
<a href="http://twitter.com/share?url=http://stravafriends.cd34.com/&text=Find riders that have ridden the Strava segments you've ridden" class="twitter-share-button" data-count="horizontal">Tweet</a>
</div>
<div style="float:left;">
<div id="fb-root"></div>
<fb:like href="http://stravafriends.cd34.com/" width="250" show_faces="false" font="" layout="button_count" action="recommend"></fb:like>
</div>
</div>
</%def>
