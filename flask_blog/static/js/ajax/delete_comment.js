
$(document).on("click", "*[data-deletecomment]", (e) => {
    let commentID = $(e.target).data("commentid")
    let postID = $(e.target).data("postid")
    toggleModal('deleteComment-modal', true);
    $("#deleteComment-modal").data("commentid", commentID)
    $("#deleteComment-modal").data("postid", postID)
})

$(document).on("click", "#confirmDeleteComment", (e) => {
    let commentID = $("#deleteComment-modal").data("commentid")
    let postID = $("#deleteComment-modal").data("postid")
    $("#loaderModalContent").html("Deleteing comment...")
    toggleModal('deleteComment-modal', false);
    toggleModal('loader-modal', true)
    $.ajax({
        type: "GET",
        url: `/delete-comment/${commentID}/${postID}`,
        cache: false,
        success: function (data) {
            let counter = parseInt($("#commentCounter").text()) - 1
            $("#commentCounter").html(counter)
            $(`#commentid-${commentID}`).remove()
            
            toggleModal('loader-modal', false)
        }
    });
})