import "../css/style.css"
import "flowbite"
const validate = require("validate.js")


let constraints = {
    confirmPassword: {
        equality: "password"
    }
}

$("#confirm_password").on("input", (e) => {
    let password = $("#password").val()
    let confirmPassword = $(e.target).val();
    console.log(validate({password: password, confirmPassword: confirmPassword}, constraints));
})

// console.log();
// console.log(validate({password: "foo", confirmPassword: "test"}, constraints));