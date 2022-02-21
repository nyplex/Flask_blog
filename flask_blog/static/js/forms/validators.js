export let formValidator = {
    topicTitle: {
        length: {
            minimum: 5,
            maximum: 50,
        },
    },
    topicBody: {
        length: {
            minimum: 10,
            maximum: 10000,
        },
    },
    username: {
        length: {
            minimum: 2,
            maximum: 15,
        },
        format: {
            pattern: /^[A-Za-z0-9]+$/
        }
    },
    fname: {
        length: {
            minimum: 2,
            maximum: 15,
        },
        format: {
            pattern: /^[A-Za-z]+$/
        }
    },
    lname: {
        length: {
            minimum: 2,
            maximum: 15
        },
        format: {
            pattern: /^[A-Za-z]+$/
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
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,40}$/
        }
    },
    confirm_password: {
        equality: "original_password"
    }
}