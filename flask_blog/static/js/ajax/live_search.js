import { populateHomePage } from "./home"

let loader = `<tr>
<td colspan="4">
<div class="max-w-[80px] mx-auto" id="loader">
    <?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; background: none; display: block; shape-rendering: auto;" width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
        <circle cx="50" cy="50" r="32" stroke-width="8" stroke="#93dbe9" stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" dur="1s" repeatCount="indefinite" keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
        </circle>
        <circle cx="50" cy="50" r="23" stroke-width="8" stroke="#689cc5" stroke-dasharray="36.12831551628262 36.12831551628262" stroke-dashoffset="36.12831551628262" fill="none" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" dur="1s" repeatCount="indefinite" keyTimes="0;1" values="0 50 50;-360 50 50"></animateTransform>
        </circle>
    </svg>
    </div>
    <td>
    <tr>`

$("#posts_search").on("input", (e) => {
    $("#postsContent").html(loader)
    let value = $(e.target).val()
    let liveSearchCategory = $("#posts_search").data("livesearchcategory")
    let liveSearchUser = $("#posts_search").data("livesearchuser") 
    $.ajax({
        type: 'POST',
        url: '/live-search',
        data: {
            'input': value, 
            'liveSearchCategory': liveSearchCategory,
            'liveSearchUser': liveSearchUser
        },
        success: function (response) {
            $("#loader").addClass("hidden")
            $("#countResult").text(response.total + " Results")
            populateLiveSearch(response.data)
        }
    })
})

export let populateLiveSearch = (data) => {
    let html = ""
    // for each post in the data object 
    data.forEach(post => {
        
        //parse the JSON data into an obj
        post = JSON.parse(post)[0]
        // get the html for each tag contained in a post
        let tags = ""
        post.tags.forEach(tag => {
            tags += `<span class="primary-tags"><i class="fa-solid fa-hashtag"></i>${tag}</span>`
        });
        // Capitalize the category of the post 
        let category = post.category.category_name.trim().replace(/^\w/, (c) => c.toUpperCase())
        // declare html conttent of the post
        let category_url = ""
        if($("#posts_search").data("livesearchuser") == "all") {
            category_url = `/categories/${post.category._id.$oid}`
        }else{
            category_url = `${post.author._id.$oid}/categories/${post.category._id.$oid}`
        }
        html += `
            <tr id="post_template">
                <!--  Topic Col -->
                <td class="py-4 px-2 text-sm font-medium text-gray-900 dark:text-white text-center">
                    <div class="flex flex-row justify-left items-center">
                        <!-- Author Avatar -->
                        <img class="rounded-full mr-4 w-10 h-10" src="https://nyplex-flask-blog.s3.amazonaws.com/static/media/profile_pics/${post.author.image}" alt="">
                        <div class="flex flex-col w-full space-y-2">
                            <!-- Topic Title -->
                            <a href="/posts/${post._id.$oid}" class="text-left hover:text-blue-700 text-lg">${post.title}</a>
                            <!-- Topic Tags -->
                            <div class="flex flex-row flex-wrap gap-2">
                                ${tags}
                            </div>
                        </div>
                    </div>
                </td>
                <!-- Category Col -->
                <td class="hidden lg:table-cell py-4 px-2 text-sm font-medium text-gray-500 dark:text-white text-center">
                    <!-- Topic Category -->
                    <a href="${category_url}">
                        <span class="category-label-${post.category.category_color}">${category}</span>
                    </a>
                </td>
                <!-- Like Col -->
                <td class="hidden lg:table-cell py-4 px-2 text-sm font-medium text-gray-900 dark:text-white text-center">
                    <span>${post.like}</span><i class="fa-solid fa-thumbs-up ml-2"></i>
                </td>
                <!-- Activity Col -->
                <td class="py-4 px-2 text-sm font-medium text-gray-500 dark:text-white text-center">
                    <span class="text-gray-600">${post.posted_date}</span>
                </td>
            </tr>
        `
    });
    //Append the html content of each post to the main table container
    $("#postsContent").html(html)
}



// <!-- Topic Category -->
// {% if profile %}
// <a href="{{ url_for('users.profile', user_id=post['author']._id, category_id=post['category']._id) }}">
//     <span class="category-label-{{ post['category'].category_color }}">{{ post['category'].category_name|capitalize}}</span>
// </a>
// {% else %}
// <a href="{{ url_for('main.home', category_id=post['category']._id) }}">
//     <span class="category-label-{{ post['category'].category_color }}">{{ post['category'].category_name|capitalize}}</span>
// </a>
// {% endif %}