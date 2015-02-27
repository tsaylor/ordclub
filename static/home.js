function shortlong() {
    if ($(this).nextUntil('.short_profile').hasClass('hidden')) {
        $('.long_profile').addClass('hidden')
        $(this).nextUntil('.short_profile').removeClass('hidden') // only the next long profile
    } else {
        $(this).nextUntil('.short_profile').addClass('hidden') // only the next long profile
    }
}

function attach_click_handlers() {
    $('.people li').click(shortlong)
}

function render_profile(profile) {
    var source = $('#profile_template').html();
    var template = Handlebars.compile(source);
    var html = template(profile);
    $('.people').append(html);
}

function get_profiles_for_search(term) {
    $.get('/api/profiles/', function (data, textStatus, jqXHR) {
        for (idx in data) {
            render_profile(data[idx]);
        }
        attach_click_handlers();
    })
}

