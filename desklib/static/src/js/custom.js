$(window).on("scroll", function() {
    if($(window).scrollTop() > 100) {
        $(".navbar").addClass("navbar-light bg-light");
    } else {
        //remove the background property so it comes transparent again (defined in your css)
       $(".navbar").removeClass("navbar-light bg-light");
    }
});