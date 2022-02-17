const validate = require("validate.js")
import {
    signupValidator
} from "./validators.js"


$("#fname, #lname, #email, #confirm_email, #password, #confirm_password").on("input", (e) => {
    let check;
    switch (e.target.id) {
        case "fname":
            check = validate({
                fname: $(e.target).val()
            }, signupValidator)
            break;
        case "lname":
            check = validate({
                lname: $(e.target).val()
            }, signupValidator)
            break;
        case "email":
            check = validate({
                email: $(e.target).val()
            }, signupValidator)
            break;
        case "confirm_email":
            check = validate({
                email: $("#email").val(),
                confirm_email: $(e.target).val()
            }, signupValidator)
            break;
        case "password":
            check = validate({
                password: $(e.target).val()
            }, signupValidator)
            break;
        case "confirm_password":
            check = validate({
                password: $("#password").val(),
                confirm_password: $(e.target).val()
            }, signupValidator)
            break;
        default:
            break;
    }
    if (check) {
        $(e.target).removeClass("form-input form-valid-input").addClass("form-invalid-input")
        console.log(check);
    } else {
        $(e.target).removeClass("form-input form-invalid-input").addClass("form-valid-input")
        console.log("valid input");
    }
})