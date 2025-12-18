/*!
 * Start Bootstrap - Freelancer Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function () {
    $('body').on('click', '.page-scroll a', function (event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 800, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Highlight the top nav as scrolling occurs
$('body').scrollspy({
    target: '.navbar-fixed-top'
})

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function () {
    $('.navbar-toggle:visible').click();
});

$("#btn-generate").click(function () {
    $(".number").addClass("shake");
    setTimeout(function () {
        $(".number").removeClass("shake");
    }, 500);

    var useFrequency = $("#chk-frequency").is(":checked");
    var useMissing = $("#chk-missing").is(":checked");
    var useGaps = $("#chk-gaps").is(":checked");
    var qnt = $("#qnt-selector").val();

    var url = "/generate?use_frequency=" + useFrequency + "&use_missing=" + useMissing + "&use_gaps=" + useGaps + "&qnt=" + qnt;

    $.getJSON(url)
        .done(function (data) {
            var container = $("#numbers-container");
            container.empty();

            data.numbers.forEach(function (num, index) {
                var div = $("<div>");
                var span = $("<span>").addClass("number shake").text(num);
                div.append(span);
                container.append(div);
            });
            setTimeout(function () {
                $(".number").removeClass("shake");
            }, 500);
        })
})

$("#qnt-selector").change(function () {
    var val = $(this).val();
    var chkGaps = $("#chk-gaps");
    if (val != "6") {
        chkGaps.prop('checked', false);
        chkGaps.prop('disabled', true);
        chkGaps.parent().addClass('disabled');
    } else {
        chkGaps.prop('disabled', false);
        chkGaps.prop('checked', true);
        chkGaps.parent().removeClass('disabled');
    }
});