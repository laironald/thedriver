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

$(".publish").click(function() {
    alert("publish");
});
$(".preview").click(function() {
    url = "/preview/" + $(this).data("url");
    $.ajax({
        url: url,
        success: function(result) {
            $(".modal-body").html(result);
            $("#previewModal").modal({
                keyboard: true
            });
        }
    });
});
