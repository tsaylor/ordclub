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