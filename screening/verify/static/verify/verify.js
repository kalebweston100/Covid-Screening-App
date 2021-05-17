$(document).ready(function()
{
    const verify = {
        delimiters: ['[[', ']]'],

        template: '#verify',

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
            verifyAccount: function()
            {
                if (this.username && this.password)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'complete/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'username' : this.username, 'password' : this.password}
                    })
                    .done(function(data)
                    {
                        self.message = 'Account Verified';
                        setTimeout(() => {window.location.replace('/');}, 3000)
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Unauthorized')
                        {
                            self.message = 'Username or password is incorrect';
                        }
                        else if (error == 'Bad Request')
                        {
                            self.message = 'Data is invalid';
                        }
                        else 
                        {
                            self.message = 'Error verifying account';
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


    const routes = [
        {path: '/', component: verify, name: 'verify'}
    ]

    const router = new VueRouter({
        routes
    })

    const app = new Vue({
        router
    }).$mount('#app')

})