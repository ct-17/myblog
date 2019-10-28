$(document).ready(function(){
    // Check or Uncheck All checkboxes
    $("#action-toggle").change(function(){
        var checked = $(this).is(':checked');
        if (checked){
            $(".action-select").each(function(){
                $(this).prop("checked", true);
            });
        }
        else {
            $(".action-select").each(function(){
                $(this).prop("checked",false);
            });
        }
    });

    // Changing state of CheckAll checkbox
    $(".action-select").click(function(){
        if ($(".action-select").length == $(".action-select:checked").length){
            $("#action-toggle").prop("checked", true);
        }
        else {
            $("#action-toggle").removeAttr("checked");
        }
    });
})

