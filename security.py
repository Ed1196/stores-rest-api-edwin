from werkzeug.security import safe_str_cmp

from models.user import UserModel

#Authentication function that will check a username and password
#Gets triggered when we use the '/auth' endpoint
def authenticate(username, password):
    user = UserModel.findByUserName(username)
    #It is not safe to compare strings using == do to different systems and pyhton versions
    #if user is not None and password == user.password:
    if user and safe_str_cmp(password, user.password):
        return user

#JWT has a unique function 'identity(payload)'
    #payload: it's the contents of the JWT token, from where we can extract a username from
def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)
