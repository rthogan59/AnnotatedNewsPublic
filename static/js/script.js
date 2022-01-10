
$(document).ready(function(){
        resize();
        $(window).scroll(function(){
                checkScrollDisplays();
        });
});


function resize() {
        var pageHeight = $(window).height();
        var headerHeight = $("#header").height();
        $(".title").css("margin-top",pageHeight/10);

}

function checkScrollDisplays() {
        var scrollHeight = $(window).scrollTop();
        if(scrollHeight > $("#header").height() ){
                $("#thisPage").fadeIn("slow");
        } else {
                $("#thisPage").fadeOut("fast");
        }
}
