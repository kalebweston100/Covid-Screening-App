$(document).ready(function()
{
    const login = {
        delimiters: ['[[', ']]'],

        template: '#login',

        data: function()
        {
            return {
                username: '',
                password: '',
                message: ''
            }
        },

        methods: 
        {
            login: function()
            {
                if (this.username && this.password)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();

                    $.ajax({
                        url: 'login-user/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'username' : this.username, 'password' : this.password}
                    })
                    .done(function(data)
                    {
                        if (data.admin == true)
                        {
                            window.location.replace('edit/');
                        }
                        else if (data.admin == false)
                        {
                            window.location.replace('user/');
                        }
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            self.message = 'The data you entered was invalid';
                        }
                        else if (error == 'Unauthorized')
                        {
                            self.message = 'Your username or password is incorrect';
                        }
                        else if (error == 'Conflict')
                        {
                            var error_message = xhr.responseJSON.error_message;
                            if (error_message == 'inactive')
                            {
                                self.message = 'Your company has been temporarily deactivated. ' + 
                                               'Please contact the admin'
                            }
                            else if (error_message == 'unverified')
                            {
                                self.message = 'Your account has not been verified yet, ' + 
                                               'please follow the link in the email sent ' +
                                               'to you and enter your username and password ' +
                                               'in order to verify it';
                            }   
                        }
                        else
                        {
                            self.message = 'Error logging in';
                        }
                    })
                }
                else
                {
                    this.message = 'Please make sure both fields are filled';
                }
            }
        }
    }

    
    const key = {

        delimiters: ['[[', ']]'],

        template: '#company_key',

        data: function()
        {
            return {
                company_key: '',
                message: ''
            }
        },

        methods: 
        {
            checkKey: function()
            {
                if (this.company_key)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();

                    $.ajax({
                        url: 'check-key/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'key' : this.company_key}
                    })
                    .done(function(data)
                    {
                        if (data.message == 'valid')
                        {
                            router.push({name: 'create-user', params: {send_key: self.company_key, data_name: data.name}});
                        }
                        else if (data.message == 'inactive')
                        {   
                            self.message = "The name of the company related to that Company Key is '" + data.name + "'" + 
                                           ', but that company is not currently active. Users cannot create accounts for inactive companies. ' +
                                           'Please contact the admin of the company';
                        }
                        else if (data.message == 'unverified')
                        {
                            self.message = "The name of the company related to that Company Key is '" + data.name + "'" + 
                                        ", but that company's account has not been verified yet. Users cannot create accounts for " +
                                        "unverified companies. Please contact the admin of the company";
                        }
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            self.message = 'The data entered is invalid';
                        }
                        else if (error == 'Not Found')
                        {
                            self.message = 'There is no company with that Company Key';
                        }
                        else
                        {
                            self.message = 'Error checking Company Key';
                        }
                    })
                }
                else
                {
                    this.message = 'Please make sure the Company Key field is filled';
                }
            }
        }
    }


    const createUser = {
        delimiters: ['[[', ']]'],

        template: '#create_user',

        props: ['send_key', 'data_name'],

        data: function()
        {
            return {
                first_name: '',
                last_name: '',
                username: '',
                password: '',
                confirm_password: '',
                email: '',

                valid_password: false,
                filled: false,

                key: '',
                company_name: '',

                password_message: '',
                message: ''
            }
        },

        beforeMount: function()
        {
            if (this.send_key && this.data_name)
            {
                this.key = this.send_key;
                this.company_name = this.data_name;
            }
            else
            {
                router.push({name: 'key'});
            }
        },

        methods: 
        {
            checkMatch: function()
            {
                if (this.password && this.confirm_password)
                {
                    if (this.password == this.confirm_password)
                    {
                        if (this.checkPasswordStrength())
                        {
                            this.valid_password = true;
                            this.password_message = '';
                        }
                        else
                        {
                            this.valid_password = false;
                            this.password_message = "Your password must be a minimum of 10 characters long and " + 
                                                    "include a capital letter, number, and one of the following " + 
                                                    "special characters: !@#$%&?";
                        }
                    }
                    else
                    {
                        this.valid_password = false;
                        this.password_message = "Passwords don't match";
                    }
                }
            },

            checkPasswordStrength: function()
            {
                var valid = false;
                var regex = /[A-Z+0-9+]/;
                var special_regex = /[!@#$%&?+]/;

                if (regex.test(this.password) && special_regex.test(this.password) && this.password.length >= 10)
                {
                    valid = true;
                }
                return valid;
            },

            checkFilled: function()
            {
                if (this.first_name && this.last_name && this.username && this.password && this.confirm_password && this.email)
                {
                    this.filled = true;
                }
                else
                {
                    this.filled = false;
                }
            },

            create: function()
            {
                if (this.filled && this.valid_password)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'create-user/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'first_name' : this.first_name, 'last_name' : this.last_name,
                            'username' : this.username, 'password' : this.password, 'validate_email' : this.email,
                            'key' : this.key}
                    })
                    .done(function(data)
                    {
                        self.message = 'Your account has been created. An email with a link to a verification page ' +
                                       'has been sent to you. Enter your username and password on that page ' +
                                       'to verify your account';
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            var error_message = xhr.responseJSON.error_message;
                            if (error_message == 'invalid')
                            {
                                self.message = 'The data you entered is invalid';
                            }
                            else if (error_message == 'client_exists')
                            {
                                self.message = 'There is already an account using that email for this company';
                            }
                            else if (error_message == 'unverified')
                            {
                                self.message = 'There is an unverified account using this email. ' +
                                               'You must verify that account before you create another one'
                            }
                        }
                        else if (error == 'Conflict')
                        {
                            self.message = 'That username is taken, please choose another';
                        }
                        else if (error == 'Not Found')
                        {
                            self.message = 'The entered email address is invalid.';
                        }
                        else
                        {
                            self.message = 'Error creating account';
                        }
                    })
                }
                else
                {
                    this.message = 'Please make sure all fields are filled and your password is valid';
                }
            }
        }
    }


    const registerCompany = {
        delimiters: ['[[', ']]'],

        template: '#register_company',

        data: function()
        {
            return {
                company_name: '',
                email: '',
                confirm_email: '',
                username: '',
                password: '',
                confirm_password: '',
                email_match: false,
                valid_password: false,
                filled: false,
                email_message: '',
                password_message: '',
                message: '',
            }
        },

        methods: 
        {
            checkEmailMatch: function()
            {
                if (this.email && this.confirm_email)
                {
                    if (this.email == this.confirm_email)
                    {
                        this.email_match = true;
                        this.email_message = '';
                    }
                    else
                    {
                        this.email_match = false;
                        this.email_message = "Emails don't match";
                    }
                }
            },

            checkPasswordMatch: function()
            {
                if (this.password && this.confirm_password)
                {
                    if (this.password == this.confirm_password)
                    {
                        if (this.checkPasswordStrength())
                        {
                            this.valid_password = true;
                            this.password_message = '';
                        }
                        else
                        {
                            this.valid_password = false;
                            this.password_message = "Your password must be a minimum of 10 characters long and " + 
                                                    "include a capital letter, number, and one of the following " + 
                                                    "special characters: !@#$%&?";
                        }
                    }
                    else
                    {
                        this.valid_password = false;
                        this.password_message = "Passwords don't match";
                    }
                }
            },

            checkPasswordStrength: function()
            {
                var valid = false;
                var regex = /[A-Z+0-9+]/;
                var special_regex = /[!@#$%&?+]/;

                if (regex.test(this.password) && special_regex.test(this.password) && this.password.length >= 10)
                {
                    valid = true;
                }
                return valid;
            },

            checkFilled: function()
            {
                if (this.company_name && this.email && this.confirm_email && this.username && this.password && this.confirm_password)
                {
                    this.filled = true;
                }
                else
                {
                    this.filled = false;
                }
            },

            registerCompany: function()
            {
                if (this.filled && this.email_match && this.valid_password)
                {
                    this.email_message = '';
                    this.password_message = '';

                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'register/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'name' : this.company_name, 'validate_email' : this.email, 'username' : this.username, 'password' : this.password},
                    })
                    .done(function(data)
                    {
                        self.message = 'You have been sent an email with a link to a verification page.' +
                                       ' Enter your username and password on that page to verify your account';
                                           
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            var error_message = xhr.responseJSON.error_message;
                            if (error_message == 'invalid')
                            {   
                                self.message = 'The data you entered is invalid';
                            }
                            else if (error_message == 'previous')
                            {
                                self.message = 'You have already used this email to register a company';
                            }
                        }
                        else if (error == 'Not Found')
                        {
                            self.message = 'Your email could not be found';
                        }
                        else if (error == 'Conflict')
                        {
                            self.message = 'That username is taken, please choose another';
                        }
                        else
                        {
                            self.message = 'Error registering your account';
                        }
                    })
                }
                else
                {
                    this.message = 'Please make sure all fields are filled and you have confirmed your email and password';
                }
            }
        }
    }
    

    const routes = [
        {path: '/', component: login, name: 'login-user'},
        {path: '/key', component: key, name: 'key'},
        {path: '/create-user', component: createUser, name: 'create-user', props: true},
        {path: '/register', component: registerCompany, name: 'register-company'}
    ]

    const router = new VueRouter({
        routes
    })

    const app = new Vue({
        router
    }).$mount('#app')
})