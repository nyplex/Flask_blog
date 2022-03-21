import { delete_comment } from "./delete_comment"
import { populateComments } from "./populateComments"
let counter = 0

$("#commentsBtn").on("click", (e) => {
    let postID = $("#commentsBtn").data("postid")
    $("#addCommentBtn").toggleClass("hidden")
    $("#loadingBtnContainer").addClass("hidden")
    counter = 0
    // Ajax call to server
    if($("#commentsContainer").hasClass("hidden")) {
        $("#loader").removeClass("hidden")
        $("#commentsContainer").removeClass("hidden")
        $.ajax({
            type: 'POST',
            url: `/load-comments`,
            cache: false,
            data: {
                'c': counter, // pass the counter as url paramters
                'postID': postID,
                'limit': 2
            },
            success: function (response) {
                $("#loader").addClass("hidden")
                populateComments(response)
                if(counter + 2 > response.total) {
                    $("#noMoreComment").removeClass("hidden")
                    $("#loadingBtnContainer").addClass("hidden")
                }else{
                    $("#loadingText").text("View more comments")
                    $("#loadingIcon").addClass("hidden")
                }
                
            }
        })
    }else{
        $("#commentsContainer").addClass("hidden")
        $("#commentsContainer").empty()
        $("#noMoreComment").addClass("hidden")
    }
})

$("#loadingCommentsBtn").on("click", (e) => {
    counter += 3
    let postID = $("#commentsBtn").data("postid")
    // update the loading btn state
    $("#loadingText").text("Loading...")
    $("#loadingIcon").removeClass("hidden")
    // Ajax call to server
    $.ajax({
        type: 'POST',
        url: '/load-comments',
        data: {
            'c': counter, // pass the counter as url paramters
            'postID': postID,
            'limit': 3
        },
        success: function (response) {
            $("#loader").addClass("hidden")
            populateComments(response)
            if(counter + 3 > response.total) {
                $("#loadingBtnContainer").addClass("hidden")
                $("#noMoreComment").removeClass("hidden")
            }
            
            $("#loadingText").text("View more comments")
            $("#loadingIcon").addClass("hidden")
        }
    })
})