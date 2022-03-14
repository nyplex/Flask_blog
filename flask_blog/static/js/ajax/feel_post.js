
$('*[data-postfeelings]').on("click", (e) => {
    let feeling = $(e.target).data("postfeelings")
    let postID = $(e.target).data("postid")

    $.ajax({
        type: 'GET',
        url: `/like-post/${postID}/${feeling}`,

        success: function (response) {
            $("#likeCount").text(response['like'])
            $("#dislikeCount").text(response['dislike'])
            $("#loveCount").text(response['love'])
            if(feeling == "like"){
                $(e.target).toggleClass("likeBtnActive likeBtn")
                $('*[data-postfeelings="dislike"]').removeClass("likeBtnActive")
                $('*[data-postfeelings="dislike"]').addClass("likeBtn")
                $('*[data-postfeelings="love"]').removeClass("loveBtnActive")
                $('*[data-postfeelings="love"]').addClass("loveBtn")
            }else if(feeling == "dislike") {
                $(e.target).toggleClass("likeBtnActive likeBtn")
                $('*[data-postfeelings="like"]').removeClass("likeBtnActive")
                $('*[data-postfeelings="like"]').addClass("likeBtn")
                $('*[data-postfeelings="love"]').removeClass("loveBtnActive")
                $('*[data-postfeelings="love"]').addClass("loveBtn")
            }else if(feeling == "love") {
                $(e.target).toggleClass("loveBtnActive loveBtn")
                $('*[data-postfeelings="like"]').removeClass("likeBtnActive")
                $('*[data-postfeelings="like"]').addClass("likeBtn")
                $('*[data-postfeelings="dislike"]').removeClass("likeBtnActive")
                $('*[data-postfeelings="dislike"]').addClass("likeBtn")
            }
        }
    })
})
