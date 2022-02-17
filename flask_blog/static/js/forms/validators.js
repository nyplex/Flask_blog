export let signupValidator = {
    fname: {
        length: {
            minimum: 2,
            maximum: 15,
        },
    },
    lname: {
        length: {
            minimum: 2,
            maximum: 15
        }
    },
    email: {
        length: {
            maximum: 50
        },
        email: true
    },
    confirm_email: {
        equality: "email"
    },
    password: {
        length: {
            minimum: 6,
            maximum: 40
        },
        format: {
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,40}$/g,
            message: "can only contain a-z and 0-9"
        }
    },
    confirm_password: {
        equality: "password"
    }
}