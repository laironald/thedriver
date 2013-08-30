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
        // doc looks like:
        // description: ""
        // embedUrl: "https://docs.google.com/document/d/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/preview"
        // iconUrl: "https://ssl.gstatic.com/docs/doclist/images/icon_11_document_list.png"
        // id: "1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4"
        // lastEditedUtc: 1377551977900
        // mimeType: "application/vnd.google-apps.document"
        // name: "Testing"
        // serviceId: "doc"
        // type: "document"
        // url: "https://docs.google.com/document/d/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/edit?usp=drive_web"

        url = "/action/open_doc/" + doc["id"];
        $.ajax({
            url: url,
            success: function() {
                alert("done!");
                analytics_status = "success";
            },
            error: function() {
                analytics_status = "failure";
            },
            complete: function() {
                analytics.track("Used GoogleDoc Picker",
                    { url: url, status: analytics_status });
            }
        });
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
$("#from_google").click(function() {
    createPicker();
});
