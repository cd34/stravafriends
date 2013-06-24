<%inherit file="template.mako"/>

<%def name="title()">
</%def>

<%def name="body()">
<h2>Generating results</h2>
<p>These riders have ridden the same segments you have within
the last 30 days.</p>
<div id='results'>Loading...</div>
<script type="text/javascript">
function objectSize(obj) {
  var count = 0;
  for (var k in obj) {
    if (obj.hasOwnProperty(k)) ++count;
  }
  return count;
}
var opts = {lines: 13, length: 7, width: 4, radius: 10, rotate: 0, color: '#000', speed: 1, trail: 60, shadow: false, hwaccel: false, className: 'spinner', zIndex: 2e9, top: 'auto', left: 'auto'};
var target = document.getElementById('results');
var spinner = new Spinner(opts).spin(target);
json = $.getJSON('/strava_id/${id}', function(data) {
spinner.stop();
  if (objectSize(data.riders) > 0) {
    $('#results').html('<table id="result_table" class="table table-striped">'+
        '<tr><th>Rider\'s Name</th></tr></table>'); 
  $.each(data.riders, function(key, val) {
    $('#result_table tr:last').after('<tr><td><a href="http://app.strava.com/athletes/' + key + '" target="_blank">' + val + '</a></td></tr>');
  });
  } else {
    $('#results').html('No results found...'); 
  };
});
</script>
</%def>

<%def name="head_js()">
<script type="text/javascript" src="/static/spin.min.js"></script>
<script type="text/javaScript" src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
</%def>
