$(document).ready(function() {
  $('#postform').submit(function(e) {
  alert("heree")
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/post/',
    data: 'dssj',
    dataType: 'json',
    success: function() {}
 });
 return false;
 });
});
