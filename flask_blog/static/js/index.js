import "../css/style.css"
import "flowbite"
import "./forms/forms"
import "./forms/settings"


//Close the flash message when user click on the cls btn
$("#flash_message_btn").on("click", (e) => {
    $("#flash_message").hide()
})
//if flash message exists, close it after 5sec
if($("#flash_message").length) {
    setTimeout(() => {
        $("#flash_message").animate({opacity: 0}, 1000)
    }, 5000)
}