"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        """
        This is an example of loading a model.
        Every controller has access to the load_model method.
        """
        self.load_model('User')
        self.db = self._app.db

        """

        This is an example of a controller method that will load a view for the client

        """

    def index(self):

        return self.load_view('index.html')

    def create(self):
        user_info = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_pw': request.form['confirm_pw'],
        }

        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            session['user_id'] = create_status['user']['user_id']
            session['fname']=create_status['user']['first_name']
            session['lname'] = create_status['user']['last_name']

            return redirect('/users/success')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def login(self):
        login_info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        login_result = self.models['User'].login_user(login_info)
        if login_result == False:
            flash("Your email or password is incorrect, please try again!", 'login_errors')
            return redirect('/')
        else:
            return redirect('/users/success')


    def success(self):
        return self.load_view('success.html')




