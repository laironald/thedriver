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

    // A simple callback implementation.
    function pickerCallback(data) {
      if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
        var doc = data[google.picker.Response.DOCUMENTS][0];
        url = "/action/open_doc/" + doc["id"];
        $.ajax({
            url: url,
            dataType: "json",
            success: function(data) {
                analytics_status = "success";
                if (data["status"]) {
                    // how do we open this modal and set it up properly?
                    // $("#settingModal").modal();
                    current_url = location.href;
                    current_doc = _.last(current_url.split("/"));
                    location.href = current_url.replace("/"+current_doc, "/"+doc["id"]);
                }
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
