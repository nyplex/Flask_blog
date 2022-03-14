import { populateComments } from "./populateComments"
let counter = 0

$("#commentsBtn").on("click", (e) => {
    counter += 5
    let postID = $("#commentsBtn").data("postid")
    $("#addCommentBtn").toggleClass("hidden")
    // $("#loadingText").text("Loading...")
    // $("#loadingIcon").removeClass("hidden")
    // Ajax call to server
    if($("#commentsContainer").hasClass("hidden")) {
        $("#commentsContainer").removeClass("hidden")
        $.ajax({
            type: 'GET',
            url: `/load-comments/${postID}`,
    
            success: function (response) {
                populateComments(response)
            }
        })
    }else{
        $("#commentsContainer").addClass("hidden")
        $("#commentsContainer").html("")
    }
    
})