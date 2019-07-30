$(window).on("scroll", function() {
    if($(window).scrollTop() > 100) {
        $("header").addClass("bg-white");
    } else {
        //remove the background property so it comes transparent again (defined in your css)
       $("header").removeClass("bg-white");
    }
});