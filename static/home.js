var api_url = 'https://ordclub.herokuapp.com'

// http://stackoverflow.com/a/1909508/155987
var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

function shortlong() {
    if ($(this).nextUntil('.short_profile').hasClass('hidden')) {
        $('.long_profile').addClass('hidden')
        $(this).nextUntil('.short_profile').removeClass('hidden') // only the next long profile
    } else {
        $(this).nextUntil('.short_profile').addClass('hidden') // only the next long profile
    }
}

last_search = 'dummy'

function attach_click_handlers() {
    $('.people li').click(shortlong);
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
    $.get(api_url + '/api/profiles/', {search: term}, function (data, textStatus, jqXHR) {
        for (idx in data) {
            render_profile(data[idx]);
        }
        attach_click_handlers();
        $('#loading').addClass('hidden');
    })
}

