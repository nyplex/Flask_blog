
$('*[data-postfeelings]').on("click", (e) => {
    let feeling = $(e.target).data("postfeelings")
    let postID = $(e.target).data("postid")

    if(feeling == "like"){
        let count = parseInt($("#likeCount").text()) + 1
        $(e.target).toggleClass("likeBtnActive likeBtn")
        $('*[data-postfeelings="dislike"]').removeClass("likeBtnActive")
        $('*[data-postfeelings="dislike"]').addClass("likeBtn")
        $('*[data-postfeelings="love"]').removeClass("loveBtnActive")
        $('*[data-postfeelings="love"]').addClass("loveBtn")
        $("#likeCount").text(count)
    }else if(feeling == "dislike") {
        let count = parseInt($("#dislikeCount").text()) + 1
        $(e.target).toggleClass("likeBtnActive likeBtn")
        $('*[data-postfeelings="like"]').removeClass("likeBtnActive")
        $('*[data-postfeelings="like"]').addClass("likeBtn")
        $('*[data-postfeelings="love"]').removeClass("loveBtnActive")
        $('*[data-postfeelings="love"]').addClass("loveBtn")
        $("#dislikeCount").text(count)
    }else if(feeling == "love") {
        let count = parseInt($("#loveCount").text()) + 1
        $(e.target).toggleClass("loveBtnActive loveBtn")
        $('*[data-postfeelings="like"]').removeClass("likeBtnActive")
        $('*[data-postfeelings="like"]').addClass("likeBtn")
        $('*[data-postfeelings="dislike"]').removeClass("likeBtnActive")
        $('*[data-postfeelings="dislike"]').addClass("likeBtn")
        $("#loveCount").text(count)
    }

    $.ajax({
        type: 'GET',
        url: `/like-post/${postID}/${feeling}`,

        success: function (response) {
            $("#likeCount").text(response['like'])
            $("#dislikeCount").text(response['dislike'])
            $("#loveCount").text(response['love'])
        }
    })
})
