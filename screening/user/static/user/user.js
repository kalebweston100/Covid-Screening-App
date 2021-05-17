$(document).ready(function()
{
    const newEntry = {
        delimiters: ['[[', ']]'],

        template: '#new',

        data: function()
        {
            return {
                questions: [],
                current_question: '',
                index: 0,
                bool_content: 'no',
                content: '',
                started: false,
                completed: false,
                message: ''
            }
        },

        beforeMount: function()
        {
            this.retrieve();
        },

        methods: 
        {
            start: function()
            {
                if (this.questions.length > 0)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'start/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token}
                    })
                    .done(function(data)
                    {
                        self.started = true;
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Forbidden')
                        {
                            self.message = 'For your security, your login time has expired. Please refresh the ' +
                                       'page and login again to complete your survey';
                        }
                        else
                        {
                            self.message = 'Error starting survey';
                        }                        
                    })
                }
            },

            completeCheck: function()
            {
                var time = this.getTime();

                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'complete/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'completed_time' : time}
                })
                .done(function(data)
                {
                    if (data.passed)
                    {
                        self.message = 'Your employer has determined that you are safe to go to work';
                    }
                    else
                    {
                        self.message = 'Your employer has determined that you should stay home';
                    }
                })
                .fail(function(xhr, status, error)
                {
                    var error_message = xhr.responseJSON.error_message;
                    if (error_message == 'invalid')
                    {
                        self.message = 'There was an error sending the time you completed your survey';
                    }
                    else if (error_message == 'expired')
                    {
                        self.message = 'For your security, your login time has expired. Please refresh the ' +
                                       'page and login again to complete your survey';
                    }
                    else
                    {
                        self.message = 'Error completing survey';
                    }
                })
            },

            saveEntry: function(question_number)
            {
                var send;
                var filled = false;

                if (this.current_question.bool_answer)
                {
                    send = this.bool_content;
                    filled = true;
                }
                else if (this.content)
                {
                    send = this.content;
                    filled = true;
                }
                
                if (filled)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'save-entry/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'question_number' :  question_number, 'content' : send}
                    })
                    .done(function(data)
                    {
                        self.message = 'Answer saved';
                        self.next();
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            self.message = 'Data was invalid';
                        }
                        else if (error == 'Not Found')
                        {
                            self.message = 'Some server data was not found, please refresh the page and try again';
                        }
                        else if (error == 'Forbidden')
                        {
                            self.message = 'For your security, your login time has expired. Please refresh the ' +
                                           'page and login again to complete your survey';
                        }
                        else
                        {
                            self.message = 'Error saving entry';
                        }
                    })
                }
                else
                {
                    self.message = 'Please provide an answer';
                }
            },

            retrieve: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-questions/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                })
                .done(function(data)
                {
                    self.questions = data;
                    if (data.length == 0)
                    {
                        self.message = 'No current questions';
                    }
                    else
                    {
                        self.display();
                    }
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error retrieving questions';
                })
            },

            display: function()
            {
                this.current_question = this.questions[this.index];
            },

            next: function()
            {
                this.index += 1;
                if (this.index == this.questions.length)
                {
                    this.completed = true;
                    this.completeCheck();
                }
                else
                {
                    this.display();
                }
            },
            
            getTime: function()
            {
                var rawTime = new Date().toLocaleString();
                var splitTime = rawTime.split(' ');
                var date = splitTime[0].split('/')
                var time = splitTime[1].split(':');
                
                for (var i = 0; i < 3; i++)
                {
                    if (date[i].length < 2)
                    {
                        date[i] = '0' + date[i];
                    }

                    if (time[i].length < 2)
                    {
                        time[i] = '0' + time[i];
                    }
                }

                var completedTime = date.join('/') + ' ' + time.join(':') + ' ' + splitTime[2];
                return completedTime;
            },

              
        }
    }

    const routes = [
        {path: '/', component: newEntry, name: 'new'},
    ]

    const router = new VueRouter({
        routes
    })

    const app = new Vue({
        router,

        delimiters: ['[[', ']]'],

        data: 
        {
            app_message: ''
        },

        methods:
        {
            logout: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'logout/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token}
                })
                .done(function(data)
                {
                    window.location.replace('/');
                })
                .fail(function(xhr, status, error)
                {
                    self.app_message = 'Error logging out';
                })
            } 
        }
    }).$mount('#app')
})