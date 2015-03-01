// http://stackoverflow.com/a/1909508/155987
var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

function shortlong() {
    $('.long_profile').addClass('hidden');
    var this_is_closed = $(this).hasClass('closer');
    $('.short_profile').removeClass('closer');
    if (!this_is_closed) {
        $(this).nextUntil('.short_profile').removeClass('hidden'); // open the next long profile after 'this' short_profile
        $(this).addClass('closer');
    }
}

last_search = 'dummy'

function attach_click_handlers() {
    $('.people li.short_profile').click(shortlong);
}

function render_profile(profile) {
    var source = $('#profile_template').html();
    var template = Handlebars.compile(source);
    var html = template(profile);
    $('.people').append(html);
}

function get_profiles_for_search(term) {
    $('#loading').removeClass('hidden');
    $('.people').empty();
    last_search = term;
    $.get('/api/profiles/', {search: term}, function (data, textStatus, jqXHR) {
        for (idx in data) {
            render_profile(data[idx]);
        }
        attach_click_handlers();
        $('#loading').addClass('hidden');
    })
}

