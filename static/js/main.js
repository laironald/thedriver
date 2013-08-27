// per: https://gist.github.com/aarongustafson/1313517
function adjustIframes()
{
  $('iframe').each(function(){
    var
    $this       = $(this),
    proportion  = $this.data( 'proportion' ),
    w           = $this.attr('width'),
    actual_w    = $this.width();

    if ( ! proportion )
    {
        proportion = $this.attr('height') / w;
        $this.data( 'proportion', proportion );
    }

    if ( actual_w != w )
    {
        $this.css( 'height', Math.round( actual_w * proportion ) + 'px' );
    }
  });
}
$(window).on('resize load', adjustIframes);

// Google Picker
    function createPicker() {
        var picker = new google.picker.PickerBuilder().
            addView(google.picker.ViewId.DOCUMENTS).
            setCallback(pickerCallback).
            build();
        picker.setVisible(true);
    }
    // A simple callback implementation.
    function pickerCallback(data) {
      if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
        var doc = data[google.picker.Response.DOCUMENTS][0];
        url = doc[google.picker.Document.URL];
        console.log(doc);
      }
    }

// other stuff

$(document).ready(function () {
  $('.tip').hover(function() {
    $(this).tooltip('show');
  });
});

$(".publish").click(function() {
    url = "/publish/" + $(this).data("url");
    $(".publish").attr("disabled", "disabled");
    $.ajax({
        url: url,
        dataType: "json",
        success: function() {
            $("#status_message").removeClass("alert-danger hide").addClass("alert-success").fadeIn("slow").html("Successfully Published").delay(800).fadeOut('slow');
            analytics_status = "Published success";
        },
        error: function() {
            $("#status_message").addClass("alert-danger").removeClass("hide alert-success").fadeIn("slow").html("Publishing Error: try again").delay(800).fadeOut('slow');
            analytics_status = "Published failure";
        },
        complete: function() {
            $(".publish").removeAttr("disabled");
            analytics.track(analytics_status, {url: url});
        }
    });
});
$(".preview").click(function() {
    $(".modal-header .nav-pills li").removeClass("active");
    $(".modal-header .nav-pills li.first").addClass("active");
    url = "/preview/" + $(this).data("url");
    $(".modal-body iframe").attr("src", url);
    analytics.track('Previewed document', {url: url});
});
$(".modal-header .nav-pills a").click(function() {
    $(".modal-header .nav-pills li").removeClass("active");
    $(this).parent("li").addClass("active");
    if ($(this).html() == "Preview") {
        url = "/preview/";
    } else {
        url = "/view/";
    }
    url = url + $(this).data("url");
    $(".modal-body iframe").attr("src", url);
    analytics.track('Change preview option', {url: url});
});
$("#from_google").click(function() {
    createPicker();
});
