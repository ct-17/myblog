// function OpenFormReply() {
//     document.getElementById("form_reply").style.display = "block";
//   }

$(document).ready(function(){
    function updateText(btn, newCount, verb){
        btn.html("<i class='fa fa-heart'></i> " + newCount + " | " + verb)
    }

    $(".ct-button-like").click(function(e){
        e.preventDefault()
        var this_ = $(this)
        var likeUrl = this_.attr("data-href")
        
        if (likeUrl){
            $.ajax({
                url: likeUrl,
                method: "GET",
                data: {},
                success: function(data){
                if (data.liked){
                    updateText(this_, data.total + 1, "Like")
                } else {
                    updateText(this_, data.total - 1, "Like")
                }

                }, error: function(error){
                console.log(error)
                console.log("error")
                }
            });
        }
    
    });
});

$(document).ready(function(){
    var $commentForm = $('.ajax-form-comment')
    $commentForm.submit(function(event){
        event.preventDefault();
        var $commentData = $(this).serialize()
        var $commentURL = $commentForm.attr('data-url') || window.location.href
        
        $.ajax({
            method: "POST",
            url: $commentURL,
            data: $commentData,
            success: function(data){
                if (event.originalEvent.submitter.className == "button_comment"){
                    $('.comments').load(' .comments');
                    $commentForm[0].reset();
                } else if (event.originalEvent.submitter.className == "button_reply"){
                    var class_reply = ".reply_list_" + event.originalEvent.submitter.name
                    $("".replace("",class_reply)).load( " 1".replace("1",class_reply));
                    $('[name="body"]').val('');
                } else {
                    console.log("ERROR Comment.")
                }
            },
            error: function(){
                console.log("Commnet ajax false.")
            },
        });
    });
});

// CSRF Ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
