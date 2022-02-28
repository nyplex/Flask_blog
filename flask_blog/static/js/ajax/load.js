import { populateCategories } from "./categories"
import { populateHomePage } from "./home"


let counter = 0

$("#loadingBtn, #loadingBtnCategories").on("click", (e) => {
    console.log($(location).attr('href'));
    counter += 5
    let dataAttr = $(e.target).data("loading")
    let category
    if(dataAttr == "posts") {
        category = $(e.target).data("category")
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
            'category': category
        },
        success: function (response) {
            // if counter is >= to the total of posts in the DB , no more post to load => update the loading btn
            if(counter >= response.total) {
                $("#loadingBtnContainer").html("<p class='text-white text-lg font-medium'>No more post to load</p>")
            }else{
                // populate the home page with new loaded posts
                if(dataAttr == "posts") {
                    populateHomePage(response.result)
                }else{
                    populateCategories(response.result)
                }
            }
        }
    })
})