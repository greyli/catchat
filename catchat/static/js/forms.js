$(document).ready(function () {
    // login form
    $('.login.ui.form')
        .form({
            fields: {
                email: {
                    identifier: 'email',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter your e-mail'
                    },
                        {
                            type: 'email',
                            prompt: 'Please enter a valid e-mail'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter your password'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: 'Your password must be at least 6 characters'
                        }
                    ]
                }
            }
        });

    // register form
    $('.register.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter your name'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: 'Your nickname must be not more than {ruleValue} characters'
                        }
                    ]
                },
                email: {
                    identifier: 'email',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter your e-mail'
                    },
                        {
                            type: 'email',
                            prompt: 'Please enter a valid e-mail'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter a password'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: 'Your password must be at least {ruleValue} characters'
                        }
                    ]
                },
                password2: {
                    identifier: 'password2',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter a password'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: 'Your password must be at least {ruleValue} characters'
                        },
                        {
                            type: 'match[password]',
                            prompt: 'Your confirm password must be match the value of the password field'
                        }
                    ]
                },

                terms: {
                    identifier: 'terms',
                    rules: [{
                        type: 'checked',
                        prompt: 'You must agree to the terms and conditions'
                    }]
                }
            }
        });

    // profile form
    $('.profile.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [{
                        type: 'empty',
                        prompt: 'Please enter your name'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: 'Your nickname must be not more than {ruleValue} characters'
                        }
                    ]
                },
                github: {
                    identifier: 'github',
                    optional: true,
                    rules: [{
                        type: 'url',
                        prompt: 'Please enter a valid url'
                    }]
                },
                website: {
                    identifier: 'website',
                    optional: true,
                    rules: [{
                        type: 'url',
                        prompt: 'Please enter a valid url'
                    }]
                },

                bio: {
                    identifier: 'bio',
                    optional: true,
                    rules: [{
                        type: 'maxLength[25]',
                        prompt: 'Your bio must be not more than {ruleValue} characters'
                    }]
                }
            }
        });
});
