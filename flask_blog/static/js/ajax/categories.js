let counter = 0
// Listen to user clicking on the "load more" btn
$("#loadingBtnCategories").on("click", (e) => {
    // increment counter by 5 (5 is the limit of posts loaded)
    counter += 6
    // update the loading btn state
    $("#loadingText").text("Loading...")
    $("#loadingIcon").removeClass("hidden")
    // Ajax call to server
    $.ajax({
        type: 'GET',
        url: '/categories/load',
        data: {
            'c': counter // pass the counter as url paramters
        },
        success: function (response) {
            // if counter is >= to the total of posts in the DB , no more post to load => update the loading btn
            if(counter >= response.total) {
                $("#loadingBtnContainer").html("<p class='text-white text-lg font-medium'>No more post to load</p>")
            }else{
                console.log(response);
                // populate the home page with new loaded posts
                populateCategories(response.result)
            }
        }
    })
})


//Populate the home page with the posts lodaded by the ajax call
let populateCategories = (data) => {
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
