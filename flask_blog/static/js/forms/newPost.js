let topicTags = $("#topicTags")
let tagsContainer = $("#newTopicTagsContainer")
let maxTitleLen = 50
let tags = []

// Change the max character span on title input when user type
$("#topicTitle").on("input", (e) => {
    let len = $(e.target).val().length
    let total = maxTitleLen - len
    if(total <= 0) {
        $("#topicTitleCompter").text(0)
    }else{
        $("#topicTitleCompter").text(total)
    }
    
})

// Add the tags 
// Listen to user input on the tag's input
topicTags.on("input", (e) => {
    // get the input value and get the last character
    let val = $(e.target).val()
    let last = val.charAt(val.length - 1);
    // if last character is ","
    if(last == ","){
        // remove all white space, special char. from the user input
        val = val.replace(/\s/g,'')
        val = val.replace(/[^a-zA-Z0-9]/g, "")
        val = val.trim()

        // if the tags array is less or equal to 5 , display an error 
        if(tags.length >= 5){
            topicTags.removeClass("form-input")
            topicTags.addClass("form-invalid-input")
            let invalidLabel = `<span class="font-medium">Oops! </span>Maximum 5 tags allowed`
            $("#invalid-label-tags").html(invalidLabel)
            return
        }
        // if the user's input is already in the tags array, display an error
        if(tags.includes(val)) {
            let invalidLabel = `<span class="font-medium">Oops! </span>You already used this tag`
            $("#invalid-label-tags").html(invalidLabel)
            topicTags.val(null)
            return
        }
        // if the user's input is less than 2 or more than 15 char, display an error
        if(val.length > 15 || val.length < 2) {
            let invalidLabel = `<span class="font-medium">Oops! </span>Tag must be between 2 and 15 characters long`
            $("#invalid-label-tags").html(invalidLabel)
            topicTags.val(null)
            return
        }
        // if the tags array len is less than 5, add the user's input and display the new tag under the input field
        if(tags.length < 5) {
            tag = `<span class='hover-tags'><i class='fa-solid fa-hashtag'></i>${val}</span>`
            tagsContainer.append(tag)
            tags.push(val)
            topicTags.val(null)
            $("#newTopicTags").val(tags)
            $("#invalid-label-tags").empty()
            topicTags.addClass("form-input")
            topicTags.removeClass("form-invalid-input")
            return
        }
    }
})

// Listen on the tags container for user click
tagsContainer.on("click", (e) => {
    //check if user click on a tag
    if($(e.target).prop("tagName") == "SPAN") {
        let value = $(e.target).text()
        //check if the clicked tag is inside the tag array, if yes, remove the clicked tag from the tag array and from the DOM
        if(tags.includes(value)) {
            tags = tags.filter(item => item !== value)
            $(e.target).remove()
            $("#newTopicTags").val(tags)
            $("#invalid-label-tags").empty()
            topicTags.addClass("form-input")
            topicTags.removeClass("form-invalid-input")
        }
    }
})

