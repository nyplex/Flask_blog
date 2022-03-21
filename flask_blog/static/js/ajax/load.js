import { populateCategories } from "./categories"
import { populateHomePage, populateUserPosts } from "./home"


let counter = 0

$("#loadingBtn, #loadingBtnCategories").on("click", (e) => {
    counter += 5
    let dataAttr = $(e.target).data("loading")
    let category
    let userID
    if(dataAttr == "posts") {
        category = $(e.target).data("category")
    }else if(dataAttr == "postUser") {
        category = $(e.target).data("category")
        userID = $(e.target).data("userid")
        console.log(userID);
    }else{
        category = null
    }
    // update the loading btn state
    $("#loadingText").text("Loading...")
    $("#loadingIcon").removeClass("hidden")
    // Ajax call to server
    $.ajax({
        type: 'GET',
        url: '/load',
        data: {
            'c': counter, // pass the counter as url paramters
            'coll': dataAttr,
            'category': category,
            "userid": userID
        },
        success: function (response) {
            // if counter is >= to the total of posts in the DB , no more post to load => update the loading btn
            console.log(counter);
            console.log(response.total);
            if(counter + 5 >= response.total) {
                if(dataAttr == "posts" || dataAttr == "postUser") {
                    $("#loadingBtnContainer").html("<p class='text-white text-lg font-medium'>No more post to load</p>")
                }else {
                    $("#loadingBtnContainer").html("<p class='text-white text-lg font-medium'>No more category to load</p>")
                }
            }
            // populate the home page with new loaded posts
            if(dataAttr == "posts") {
                populateHomePage(response.result)
            }else if(dataAttr == "postUser"){
                populateUserPosts(response.result)
            } else{
                populateCategories(response.result)
            }
        }
    })
})