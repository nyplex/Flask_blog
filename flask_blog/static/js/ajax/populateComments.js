export let populateComments = (response) => {
    let html = ""
    if(response['counts'] <= 0) {
        html += `
        <div>
            <h2 class="dark:text-gray-100 text-gray-800 font-medium text-center text-2xl mb-4 pl-2">No comment on this post yet</h2>
        </div>`
    }else{
        response['result'].forEach(comment => {
            comment = JSON.parse(comment)[0]
            let deleteBtn = ""
            if(comment['delete'] == true) {
                deleteBtn = `
                <div class="mt-2 flex flex-row justify-end">
                    <a href="{{ url_for('posts.delete_comment', comment_id=comment['_id'], post_id=post['_id']) }}"><button class="danger-btn py-1.5 px-2.5">DELETE</button></a>
                </div>`
            }
            html += `
            <div class="max-w-full dark:bg-gray-800 bg-gray-100 w-full rounded-lg p-4 shadow-lg mb-4">
                <div class="flex flex-row justify-between">
                    <div class="flex flex-row justify-left items-center">
                        <!-- Author Avatar -->
                        <img class="rounded-full mr-4 w-10 h-10" src="/static/media/profile_pics/${comment.author.image}" alt="">
                        <div class="flex flex-col w-full space-y-2">
                            <!-- Topic Title -->
                            <a href="/profile/${comment.author._id.$oid}" class="navbar-unactive-link text-lg font-medium">${comment['author']['username']}</a>
                        </div>
                    </div>
                    <div class="mobile:flex flex-row justify-between items-center hidden">
                        <i class="fa-solid fa-clock text-lg dark:text-gray-600 text-gray-400 mr-2"></i>
                        <span class="text-gray-600">${comment['posted_date']}</span>
                    </div>
                </div>
                <div class="mt-2">
                    <p class="font-medium text-lg dark:text-gray-100 text-gray-800">${comment['body']}</p>
                </div>
                ${deleteBtn}
            </div>`
        })
    }
    $("#commentsContainer").append(html)
}