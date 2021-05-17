$(document).ready(function()
{
    const summary = {
        delimiters: ['[[', ']]'],

        template: '#summary',

        data: function()
        {
            return {
                days: [],
                start_date: '',
                end_date: '',
                valid: true,
                total: 0,
                safe: 0,
                unsafe: 0,
                message: '',    
            }
        },

        beforeMount: function()
        {
            this.retrieveSummary();
        },

        methods: 
        {
            checkDateError: function()
            {
                if (this.start_date != '' && this.end_date == '')
                {
                    this.message = 'Please enter an end date';
                    this.valid = false;
                }
                else if (this.start_date == '' && this.end_date != '')
                {
                    this.message = 'Please enter a start date';
                    this.valid = false;
                }
                else
                {
                    this.message = '';
                    this.valid = true;
                }
            },

            clearFilter: function()
            {
                this.start_date = '';
                this.end_date = '';
                this.retrieveSummary();
                this.valid = true;
            },

            retrieveSummary: function()
            {
                if (this.valid)
                {
                    var self = this;
                    var token = $('[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url: 'retrieve-summary/',
                        method: 'POST',
                        headers: {'X-CSRFToken' : token},
                        data: {'start_date' : this.start_date, 'end_date' : this.end_date}
                    })
                    .done(function(data)
                    {
                        if (data.length > 0)
                        {
                            self.message = '';
                            self.days = self.createDays(data);
                            self.createTotals();
                        }
                        else
                        {
                            self.total = 0;
                            self.safe = 0;
                            self.unsafe = 0;
                            self.days = [];
                            self.message = 'No entries yet';
                        }  
                    })
                    .fail(function(xhr, status, error)
                    {
                        if (error == 'Bad Request')
                        {
                            self.message = 'Data is invalid';
                        }
                        else
                        {
                            self.message = 'Error retrieving summary';
                        }
                    })
                }
            },

            createTotals: function()
            {
                this.total = 0;
                this.safe = 0;
                this.unsafe = 0;

                for (var i = 0; i < this.days.length; i++)
                {
                    this.total += this.days[i].total;
                    this.safe += this.days[i].safe;
                    this.unsafe += this.days[i].unsafe;
                }
            },

            createDays: function(checks)
            {
                var days = [];
                var currentDay = startDay(checks[0]);
                for (var i = 1; i < checks.length; i++)
                {
                    if (currentDay.date == getDate(checks[i].completed_time))
                    {
                        var counts = checkPassed(checks[i]);
                        currentDay.total += 1;
                        currentDay.safe += counts[0];
                        currentDay.unsafe += counts[1];    
                    }
                    else
                    {
                        days.push(currentDay);
                        currentDay = startDay(checks[i]);
                    }
                }

                days.push(currentDay);
                return days;

                function checkPassed(check)
                {
                    var safe, unsafe;
                    if (check.passed)
                    {
                        safe = 1;
                        unsafe = 0;
                    }
                    else
                    {
                        safe = 0;
                        unsafe = 1;
                    }
                    return [safe, unsafe];
                }
                
                function startDay(check)
                {
                    var counts = checkPassed(check);
                    var day = {date: getDate(check.completed_time), total: 1, safe: counts[0], unsafe: counts[1]};
                    return day;
                }

                function getDate(completed_time)
                {
                    var splitTime = completed_time.split('T');
                    return splitTime[0];
                }
            }
        }
    }


    const answers = {
        
        delimiters: ['[[', ']]'],

        template: '#answers',

        data: function()
        {
            return {
                questions: [],
                current_number: '',
                answers: [],
                bool_question: false,
                yes_count: 0,
                no_count: 0,
                message: ''
            }
        },

        beforeMount: function()
        {
            this.retrieveQuestions();
        },

        methods: 
        {
            retrieveQuestions: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-questions/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token}
                })
                .done(function(data)
                {
                    self.questions = data;
                    if (data.length == 0)
                    {
                        self.message = 'No questions created';
                    }
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error retrieving questions';
                })
            },

            retrieveAnswers: function(question_number, bool_answer)
            {
                this.current_number = question_number;
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-answers/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'send_number' : question_number}
                })
                .done(function(data)
                {
                    self.answers = [];
                    self.bool_question = false;
                    if (data.length == 0)
                    {
                        self.message = 'No answers yet';
                    }
                    else
                    {
                        if (bool_answer)
                        {
                            self.countBoolAnswers(data);
                            self.bool_question = true;
                        }
                        else
                        {
                            self.answers = data;
                        }
                    }
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error retrieving answers';
                })
            },

            countBoolAnswers: function(answers)
            {
                var yes_count = 0;
                var no_count = 0;

                for (var i = 0; i < answers.length; i++)
                {
                    var answer = answers[i];
                    if (answer.content == 'yes')
                    {
                        yes_count += 1;
                    }
                    else if (answer.content == 'no')
                    {
                        no_count += 1;
                    }
                }

                this.yes_count = yes_count;
                this.no_count = no_count;
            }
        }
    }


    const questions = {
        delimiters: ['[[', ']]'],

        template: '#questions',

        data: function()
        {
            return {
                questions: [],
                show_save: false,
                bool_answer: true,
                notify: true,
                personal: false,
                content: '',
                confirm_remove: '',
                remove_number: '',
                message: ''
            }
        },

        beforeMount: function()
        {
            this.display();
        },

        methods: 
        {
            showSave: function()
            {
                if (this.show_save)
                {
                    this.show_save = false;
                    this.message = '';
                }
                else
                {
                    this.show_save = true;
                }
            },

            saveQuestion: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'save-question/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'content' : this.content, 'bool_answer' : this.bool_answer, 'notify' : this.notify, 'personal' : this.personal}
                })
                .done(function(data)
                {
                    self.display();
                    self.message = 'Question saved';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Please make sure the Question field is filled';
                })
            },

            handleBool: function()
            {
                if (this.bool_answer)
                {
                    this.notify = true;
                }
                else
                {
                    this.notify = false;
                    this.personal = false;
                }
            },

            handlePersonal: function()
            {
                if (this.personal)
                {
                    this.notify = true;
                }
            },

            removeQuestion: function()
            {
                this.confirm_remove = false;

                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'delete-question/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'send_number' : this.remove_number}
                })
                .done(function(data)
                {
                    self.display();
                    self.message = 'Question deleted';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error deleting question';
                })
            },

            confirmRemove: function(question_number)
            {
                this.confirm_remove = true;
                this.remove_number = question_number;
            },

            cancelRemove: function()
            {
                this.confirm_remove = false;
                this.remove_number = 0;
            },

            display: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-edit-questions/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                })
                .done(function(data)
                {
                    self.questions = data;
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error retrieving questions';
                })
            },

            addDefault: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'add-default/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token}
                })
                .done(function(data)
                {
                    self.message = 'Standard questions added';
                    self.display();
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error adding standard questions';
                })
            }
        }   
    }


    const users = {

        delimiters: ['[[', ']]'],

        template: '#users',

        data: function()
        {
            
            return {
                users: [],
                first_name: '',
                last_name: '',
                results_first: '',
                results_last: '',
                message: '',
                show_search: false,
                remove_number: 0,
                confirm_remove: false
            }
        },

        beforeMount: function()
        {   
            this.display();
        },

        methods: 
        {
            showSearch: function()
            {
                if (this.show_search)
                {
                    this.show_search = false;
                }
                else
                {
                    this.show_search = true;
                }
            },

            display: function()
            {
                if (this.first_name != '')
                {
                    this.results_first = this.first_name;
                }

                if (this.last_name != '')
                {
                    this.results_last = this.last_name;
                }

                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-users/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'first_name' : this.first_name, 'last_name' : this.last_name}
                })
                .done(function(data)
                {
                    self.users = data;
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error displaying users';
                })
            },

            clearSearch: function()
            {
                this.first_name = '';
                this.last_name = '';
                this.results_first = '';
                this.results_last = '';
                this.display();
            },

            confirmRemove: function(client_number)
            {
                this.remove_number = client_number;
                this.confirm_remove = true;
            },

            cancelRemove: function()
            {
                this.confirm_remove = false;
                this.remove_number = 0;
            },

            removeUser: function()
            {
                this.confirm_remove = false;

                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'remove-user/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'send_number' : this.remove_number}
                })
                .done(function(data)
                {
                    self.display();
                    self.message = 'User removed';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error removing user';
                })
            }
        }
    }


    const account = {
        delimiters: ['[[', ']]'],

        template: '#account',

        data: function()
        {
            return {
                company: '',
                name: '',
                password: '',
                email: '',
                confirm_change: '',
                message: ''
            }
        },

        beforeMount: function()
        {
            this.displayCompany();
        },

        methods: 
        {
            displayCompany: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'display-company/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token}
                })
                .done(function(data)
                {
                    console.log(data);
                    self.company = data;
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error retrieving company information';
                })
            },

            changeName: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'change-name/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'send_text' : this.name}
                })
                .done(function(data)
                {
                    self.displayCompany();
                    self.message = 'Company Name successfully changed';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Please make sure the Company Name field is filled';
                })
            },

            confirmChange: function()
            {
                this.confirm_change = true;
            },

            cancelChange: function()
            {
                this.confirm_change = false;
            },

            resetKey: function()
            {
                this.confirm_change = false;

                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'reset-key/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token}
                })
                .done(function(data)
                {
                    self.displayCompany();
                    self.message = 'Company Key successfully reset';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Error resetting Company Key';
                })
            },

            /*
            changePassword: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'change-password/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                    data: {'password' : this.password}
                })
                .done(function(data)
                {
                    self.displayCompany();
                    self.message = 'Password successfully changed';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'Please make sure the New Password field is filled';
                })
            },
            */

            deactivateCompany: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'deactivate/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                })
                .done(function(data)
                {
                    self.displayCompany();
                    self.message = 'Company successfully deactivated';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'There was an error deactivating your company';
                })
            },

            reactivateCompany: function()
            {
                var self = this;
                var token = $('[name=csrfmiddlewaretoken]').val();
                $.ajax({
                    url: 'reactivate/',
                    method: 'POST',
                    headers: {'X-CSRFToken' : token},
                })
                .done(function(data)
                {
                    self.displayCompany();
                    self.message = 'Company successfully reactivated';
                })
                .fail(function(xhr, status, error)
                {
                    self.message = 'There was an error reactivating your company';
                })
            }
        }
    }


    const routes = [
        {path: '/', component: summary, name: 'summary'},
        {path: '/questions', component: questions, name: 'questions'},
        {path: '/answers', component: answers, name: 'answers'},
        {path: '/users', component: users, name: 'users'},
        {path: '/account', component: account, name: 'account'}
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
            },

            formatSimpleDate: function(date)
            {
                var splitDate = date.split('-');
                var newDate = splitDate[1] + '-' + splitDate[2] + '-' + splitDate[0];
                return newDate;
            },

            formatDates: function(data)
            {
                var checks = data;
                for (var i = 0; i < checks.length; i++)
                {
                    var completedTime = checks[i].completed_time;

                    if (completedTime != null)
                    {
                        checks[i].completed_time = format(completedTime);
                    }
                }

                return checks;

                function format(completedTime)
                {
                    var splitTime = completedTime.split('T');
                    var date = splitTime[0].split('-');
                    date.push(date.splice(0, 1));
                    date = date.join('-');
                    var time = splitTime[1].split(':');
                    var timeStamp = 'am';

                    if (time[0] >= 12)
                    {
                        if (time[0] != 24)
                        {
                            timeStamp = 'pm';
                        }

                        if (time[0] != 12)
                        {
                            time[0] = time[0] - 12;
                        }
                    }

                    time = time[0] + ':' + time[1] + timeStamp;

                    var formattedTime = date + ' ' + time;
                    return formattedTime;
                }
            }
        }
    }).$mount('#app')
})
