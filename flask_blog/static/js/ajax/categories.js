

//Populate the home page with the posts lodaded by the ajax call
export let populateCategories = (response) => {
    let data = response.result
    let adminBtn = ""
    let html = ""
    // for each post in the data object 
    data.forEach(post => {
        //parse the JSON data into an obj
        post = JSON.parse(post)
        // declare html conttent of the post
        if(response.delete == true) {
            adminBtn = `<div class="flex flex-row justify-end gap-x-4">
                            <button data-editcategory data-editcategoryid="${post._id.$oid}" data-editcategorytitle="${post['category_name']}" data-editcategorybody="${post.description}" class="text-blue-500">Edit</button>
                            <button data-deletecategory data-deletecategoryid="${post._id.$oid}" class="text-red-500" type="button" data-modal-toggle="deleteCategory-modal">Delete</button>
                        </div>`
        }else{
            adminBtn = ""
        }
        html += `<div class="p-6 w-[30%] min-w-[290px] bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-700">
                    <a href="/categories/${post._id.$oid}" class="">
                        <div class="flex flex-row justify-between">
                            <span class="category-label-${post.category_color}">${post['category_name']}</span>
                            <span class="text-gray-500 font-normal text-lg">Threads - ${post.count}</span>
                        </div>
                        <div>
                            <p class="my-3 font-normal text-gray-700 dark:text-gray-400">${post.description}</p>
                        </div>
                    </a>
                    ${adminBtn}
                </div>`


    });
    $("*[data-deletecategory]").off()
    $("*[data-editCategory]").off()
    //Append the html content of each post to the main table container
    $("#categoriesContainer").append(html)
    //Update the state of the loading btn
    $("#loadingText").text("Loading more")
    $("#loadingIcon").addClass("hidden")
    //scroll down to the page after appeding the new posts
    let toScroll = $(document).height() - $(window).height()
    $("html, body").animate({ scrollTop: toScroll }, "slow")
    //Delete category
    $("*[data-deletecategory]").on("click", (e) => {
        toggleModal('deleteCategory-modal', true)
        let data = $(e.target).data("deletecategoryid")
        let url = `/delete-categories/${data}`
        $("#deleteCategoryBtn").attr("href", url)
    })
    //Edit Category
    $("*[data-editCategory]").on("click", (e) => {
        toggleModal('editCategory-modal', true)
        let title = $(e.target).data("editcategorytitle")
        let description = $(e.target).data("editcategorybody")
        let categoryID = $(e.target).data("editcategoryid")
        
        $("#EditformCategoryName").val(title)
        $("#EditformCategoryDescription").val(description)
        $("#editCategoryID").val(categoryID)
    })
}
