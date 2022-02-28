

//Populate the home page with the posts lodaded by the ajax call
export let populateCategories = (data) => {
    let html = ""
    // for each post in the data object 
    data.forEach(post => {
        //parse the JSON data into an obj
        post = JSON.parse(post)
        // TODO get the html for each popular tags in each categories
        // let tags = ""
        // post.tags.forEach(tag => {
        //     tags += `<span class="primary-tags"><i class="fa-solid fa-hashtag"></i>${tag}</span>`
        // });

        // Capitalize the category of the post 
        //let category = post.category_name.trim().replace(/^\w/, (c) => c.toUpperCase())
        // declare html conttent of the post
        html += `
        <a href="/categories/${post._id.$oid}" class="p-6 w-[30%] min-w-[290px] bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-700">
            <div class="flex flex-row justify-between">
                <span class="category-label-${post.category_color}">${post['category_name']}</span>
                <span class="text-gray-500 font-normal text-lg">Threads - ${post.count}</span>
            </div>
            <div>
                <p class="my-3 font-normal text-gray-700 dark:text-gray-400">${post.description}</p>
            </div>
            <div>
                <span class="dark:text-gray-300 text-gray-500 font-medium text-md mb-2">Popular Tags</span>
                <div>
                    <span class="primary-tags"><i class="fa-solid fa-hashtag"></i>tags1</span>
                    <span class="primary-tags"><i class="fa-solid fa-hashtag"></i>tags2</span>
                    <span class="primary-tags"><i class="fa-solid fa-hashtag"></i>tags3</span>
                </div>
            </div>
        </a>
        `
    });
    //Append the html content of each post to the main table container
    $("#categoriesContainer").append(html)
    //Update the state of the loading btn
    $("#loadingText").text("Loading more")
    $("#loadingIcon").addClass("hidden")
    //scroll down to the page after appeding the new posts
    let toScroll = $(document).height() - $(window).height()
    $("html, body").animate({ scrollTop: toScroll }, "slow")
}
