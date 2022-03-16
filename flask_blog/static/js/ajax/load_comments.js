import { delete_comment } from "./delete_comment"
import { populateComments } from "./populateComments"
let counter = 0

$("#commentsBtn").on("click", (e) => {
    counter += 5
    let postID = $("#commentsBtn").data("postid")
    $("#addCommentBtn").toggleClass("hidden")
    
    
    // Ajax call to server
    if($("#commentsContainer").hasClass("hidden")) {
        $("#loader").removeClass("hidden")
        $("#commentsContainer").removeClass("hidden")
        $.ajax({
            type: 'GET',
            url: `/load-comments/${postID}`,
            cache: false,
            success: function (response) {
                $('html, body').animate({
                    scrollTop: $("#addCommentBtn").offset().top - 200
                }, 1000);
                $("#loader").addClass("hidden")
                populateComments(response)
                //delete_comment()
            }
        })
    }else{
        $("#commentsContainer").addClass("hidden")
        $("#commentsContainer").html("")
    }
    
})