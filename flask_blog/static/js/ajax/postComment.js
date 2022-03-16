import { delete_comment } from "./delete_comment";
import { appendNewComment } from "./populateComments";


$('#commentForm').submit(function (e) {
    let postID = $("#commentForm").data("postid")
    let form = $('#commentForm').serialize()
    $("#loaderModalContent").html("Posting comment...")
    toggleModal('authentication-modal', false);
    toggleModal('loader-modal', true)
    $.ajax({
        type: "POST",
        url: `/posts/${postID}`,
        data: form, // serializes the form's elements.
        headers: {
            'X-CSRF-TOKEN':'"{{ form.csrf_token._value() }}"'
        },
        cache: false,
        success: function (data) {
            if(data === false) {
                $("#commentBody").removeClass()
                $("#commentBody").addClass("form-invalid-input")
                $("#commentBody").addClass("text-gray-800")
                return
            }else{
                $("#commentBody").removeClass("form-invalid-input")
                $("#commentBody").addClass("form-input")
                let counter = parseInt($("#commentCounter").text()) + 1
                $("#commentCounter").html(counter)
                $("#commentBody").val("")
                appendNewComment(data)
                toggleModal('loader-modal', false);
            }
            
        }
    });
    e.preventDefault(); // block the traditional submission of the form.
    
});

