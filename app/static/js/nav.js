$(document).ready(function(){
	var pathName = window.location.pathname;
	$("ul.nav li.active").removeClass("active");
	$("ul.nav li").each(function () {
		if ($(this).find("a").attr("href") == pathName) {
		$(this).addClass("active");
		}
	})
});