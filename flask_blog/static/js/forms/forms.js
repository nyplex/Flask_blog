const validate = require("validate.js")
import {
    formValidator
} from "./validators.js"


$("#fname, #lname, #email, #confirm_email, #password, #confirm_password, #username, #topicTitle, #topicBody").on("input", (e) => {
    let check;
    switch (e.target.id) {
        case "username":
            check = validate({
                username: $(e.target).val()
            }, formValidator)
            break;
        case "fname":
            check = validate({
                fname: $(e.target).val()
            }, formValidator)
            break;
        case "lname":
            check = validate({
                lname: $(e.target).val()
            }, formValidator)
            break;
        case "email":
            check = validate({
                email: $(e.target).val()
            }, formValidator)
            break;
        case "confirm_email":
            check = validate({
                email: $("#email").val(),
                confirm_email: $(e.target).val()
            }, formValidator)
            break;
        case "password":
            check = validate({
                password: $(e.target).val()
            }, formValidator)
            break;
        case "confirm_password":
            check = validate({"original_password": $("#password").val(),confirm_password: $(e.target).val()}, formValidator)
            break;
        case "topicTitle":
            check = validate({
                topicTitle: $(e.target).val()
            }, formValidator)
            break;
        case "topicBody":
            check = validate({
                topicBody: $(e.target).val()
            }, formValidator)
            break;
        default:
            break;
    }
    if (check) {
        $(e.target).removeClass("form-input form-valid-input").addClass("form-invalid-input")
    } else {
        $(e.target).removeClass("form-input form-invalid-input").addClass("form-valid-input")
    }
})
