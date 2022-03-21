export let populateComments = (response) => {
    let html = ""
    if(response['counts'] <= 0 && response['total'] <= 0) {
        html += `
        <div>
            <h2 class="dark:text-gray-100 text-gray-800 font-medium text-center text-2xl mb-4 pl-2" id="NoCommentText">No comment on this post yet</h2>
        </div>`
    }else{
        let newComments = $("*[data-newcomment]")
        let newCommentsIDs = []
        if(newComments.length > 0) {
            for(let i = 0; i < newComments.length; i++) {
                newCommentsIDs.push($(newComments[i]).data('newcomment'))
            }
        }

        response['result'].forEach(comment => {
            comment = JSON.parse(comment)[0]
            if(newCommentsIDs.includes(comment._id.$oid)) {
                return
            }
            let deleteBtn = ""
            if(comment['delete'] == true) {
                deleteBtn = `<div class="mt-2 flex flex-row justify-end"><button class="danger-btn py-1.5 px-2.5" data-deletecomment data-postid="${comment.post.$oid}" data-commentid="${comment._id.$oid}">DELETE</button></div>`
            }
            html += `
            <div class="max-w-full dark:bg-gray-800 bg-gray-100 w-full rounded-lg p-4 shadow-lg mb-4" id="commentid-${comment._id.$oid}">
                <div class="flex flex-row justify-between">
                    <div class="flex flex-row justify-left items-center">
                        <!-- Author Avatar -->
                        <img class="rounded-full mr-4 w-10 h-10" src="/static/media/profile_pics/${comment.author.image}" alt="">
                        <div class="flex flex-col w-full space-y-2">
                            <!-- Topic Title -->
                            <a href="/profile/${comment.author._id.$oid}" class="navbar-unactive-link text-lg font-medium">@${comment['author']['username']}</a>
                        </div>
                    </div>
                    <div class="mobile:flex flex-row justify-between items-center hidden">
                        <i class="fa-solid fa-clock text-lg dark:text-gray-600 text-gray-400 mr-2"></i>
                        <span class="text-gray-600">${comment['posted_date']}</span>
                    </div>
                </div>
                <div class="mt-2">
                    <p class="comment-body")>${comment['body']}</p>
                </div>
                ${deleteBtn}
            </div>`
        })
    }
    $("#commentsContainer").append(html)
    $("#loadingBtnContainer").removeClass("hidden")
    $("body, html").animate({
        scrollTop: $(document).height()}, 1000);
}

export let appendNewComment = (response) => {
    $("#NoCommentText").addClass("hidden")
    let comment = JSON.parse(response)[0]
    let deleteBtn = `<div class="mt-2 flex flex-row justify-end"><button class="danger-btn py-1.5 px-2.5" data-deletecomment data-postid="${comment.post.$oid}" data-commentid="${comment._id.$oid}">DELETE</button></div>`
    
    let html = `<div class="max-w-full dark:bg-gray-600 bg-gray-300 w-full rounded-lg p-4 shadow-lg mb-4" id="commentid-${comment._id.$oid}" data-newcomment="${comment._id.$oid}">
                <div class="flex flex-row justify-between">
                    <div class="flex flex-row justify-left items-center">
                        <!-- Author Avatar -->
                        <img class="rounded-full mr-4 w-10 h-10" src="/static/media/profile_pics/${comment.author.image}" alt="">
                        <div class="flex flex-col w-full space-y-2">
                            <!-- Topic Title -->
                            <a href="/profile/${comment.author._id.$oid}" class="navbar-unactive-link text-lg font-medium">@${comment['author']['username']}</a>
                        </div>
                    </div>
                    <div class="mobile:flex flex-row justify-between items-center hidden">
                        <i class="fa-solid fa-clock text-lg dark:text-gray-600 text-gray-400 mr-2"></i>
                        <span class="text-gray-600">${comment['posted_date']}</span>
                    </div>
                </div>
                <div class="mt-2">
                    <p class="comment-body">${comment['body']}</p>
                </div>
                ${deleteBtn}
            </div>`
    $("#commentsContainer").prepend(html)
}