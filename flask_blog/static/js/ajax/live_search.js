import { populateHomePage } from "./home"


$("#posts_search").on("input", (e) => {
    let value = $(e.target).val()
    let liveSearchCategory = $("#posts_search").data("livesearchcategory")
    $.ajax({
        type: 'POST',
        url: '/live-search',
        data: {
            'input': value, 
            'liveSearchCategory': liveSearchCategory
        },
        success: function (response) {
            populateLiveSearch(response)
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
        html += `
            <tr id="post_template">
                <!--  Topic Col -->
                <td class="py-4 px-2 text-sm font-medium text-gray-900 dark:text-white text-center">
                    <div class="flex flex-row justify-left items-center">
                        <!-- Author Avatar -->
                        <img class="rounded-full mr-4 w-10 h-10" src="/static/media/profile_pics/${post.author.image}" alt="">
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
                    <a href="/categories/${post.category._id.$oid}">
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