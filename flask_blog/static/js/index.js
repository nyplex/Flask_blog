import "../css/style.css"
import "flowbite"
import "./forms/signup"


//Make the flash message disapering after 2sec
$("#flash_message_btn").on("click", (e) => {
    $("#flash_message").hide()
})