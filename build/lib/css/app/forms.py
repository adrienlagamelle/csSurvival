""" The Flask-WTF extension uses Python classes to represent web forms.
A form class simply defines the fields of the form as class variables.

Classes:
    SearchForm - let the user search for a query
    LoginForm - user enters username, password, remember option and submit button
    RegistrationForm - user enters username, email, language, password, password2, and submit button
    CreateGroupForm - user enters name and submit button
    AddGroupMemberForm - user enters username and submit button
    EditProfileForm - user enters username, about me information, language and submit button
    ThreadForm - user create a thread with a title and Body. Hold a submit button
    CommentForm - user enters body of comment and can subscribe or unsubscribe
    GroupForm - user adds a new member
"""

from flask_wtf import FlaskForm
from css.app import database as db
from wtforms import (
    StringField,
    PasswordField,
    TextField,
    TextAreaField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
)

# other languages can be added following the same structure for expandibility
# getting the user language and selecting a dictionary from the dicts of dicts then indexing with key value
# which will be in the form Language()["key word"]
def Language():
    userLang = "en" ## FIXME
    myLanguage = {}
    lanuages = {"English":{"Search":"Search", "Username":"Username" , "Password":"Password", "Remember Me":"Remember Me", "Sign In":"Sign In", "Email":"Email",
                         "Repeat Password":"Repeat Password", "Register":"Register", "userExistsError":"A user with that username already exists.\n Please choose a different username.","emailInUse":"Email address is already in use.\n",
                         "diffEmail":"Please choose a different email address.","New group name":"New group name",
                         "Create new group":"Create new group", "groupExistError":"The group name already exists.\n Please choose a different group name.",
                         "newMember":"Add new member", "userNonExistantError":"This user does not exist.","About me":"About me", "Submit":"Submit",
                         "diffUsername":"Please use a different username.", "Title":"Title", "Body":"Body", "Comment":"Comment", "Subscribe":"Subscribe", "Unsubscribe":"Unsubscribe", "New member":"New member"}
                ,
                "French":{"Search":"Recherche", "Username":"Nom d'utilisateur" , "Password":"Mot de passe", "Remember Me":"Souviens-toi de moi", "Sign In":"Connexion", "Email":"Email",
                        "Repeat Password":"Répéter votre Mot de passe", "Register":"Registre", "userExistsError":"Un utilisateur avec ce nom existe déjà.\n Choisir un autre nom d'utilisateur.","emailInUse":"L'adresse e-mail est déjà utilisée.\n",
                        "diffEmail":"Choisissez une autre adresse e-mail.","New group name":"Nouveau nom de groupe", "Create new group":"Créer un nouveau groupe","groupExistError":"Le nom du groupe existe déjà.\n Choisir un autre nom de groupe",
                        "newMember":"Ajouter un nouveau membre", "userNonExistantError":"Cet utilisateur n'existe pas.","About me":"À propos de moi", "Submit":"Soumettre",
                        "diffUsername":"Utiliser un autre nom d'utilisateur.", "Title":"Titre", "Body":"Bloc", "Comment":"Commentaire", "Subscribe":"Souscrire", "Unsubscribe":"Se désabonner", "New member":"Nouveau membre"}
                }
    if userLang == "en":
        myLanguage = lanuages["English"]
        return myLanguage
    if userLang == "fr":
        myLanguage = lanuages["French"]
        return myLanguage


class SearchForm(FlaskForm):
    search = TextField(Language()["Search"], validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField(Language()["Username"], validators=[DataRequired()])
    password = PasswordField(Language()["Password"], validators=[DataRequired()])
    remember = BooleanField(Language()["Remember Me"])
    submit = SubmitField(Language()["Sign In"])


class RegistrationForm(FlaskForm):
    username = StringField(Language()["Username"], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    language = SelectField(
        'Language',
        choices=[
            ('en', 'English'),
            ('fr', 'French')
        ]
    )
    password = PasswordField(Language()["Password"], validators=[DataRequired()])
    password2 = PasswordField(
        Language()["Repeat Password"], validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Ensure username doesn't already exist
    def validate_username(self, username):
        user = db.user.getFromUsername(username.data)
        if user is not None:
            raise ValidationError(
                Language()["userExistsError"]
                )

    # Ensure email is not already in use
    def validate_email(self, email):
        user = db.user.getFromEmail(email.data)
        if user is not None:
            raise ValidationError(
                Language()["emailInUse"] + Language()["diffEmail"]
                )

#
class CreateGroupForm(FlaskForm):
    name = StringField(Language()["New group name"], validators=[DataRequired()])
    submit = SubmitField(Language()["Submit"])
    def validate_name(self, name):
        groupName = db.group.getFromName(name.data)
        if groupName is not None:
            raise ValidationError(
            Language()["groupExistError"]
            )


class AddGroupMemberForm(FlaskForm):
    username = StringField(Language()["Username"], validators=[DataRequired()])
    submit = SubmitField(Language()["Submit"])
    def validate_username(self, username):
        user = db.user.getFromUsername(username.data)
        if user == None:
            raise ValidationError(
                Language()["userNonExistantError"]
            )

class EditProfileForm(FlaskForm):
    username = StringField(Language()["Username"], validators=[DataRequired()])
    about = TextAreaField(Language()["About me"], validators=[Length(min=0, max=140)])
    language = SelectField(
        'Language',
        choices=[
            ('en', 'English'),
            ('fr', 'French')
        ]
    )
    submit = SubmitField(Language()["Submit"])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.user.getFromUsername(username.data)
            if user is not None:
                raise ValidationError(Language()["diffUsername"])

class ThreadForm(FlaskForm):
    title = StringField(Language()["Title"], validators=[DataRequired()])
    body = TextAreaField(Language()["Body"], validators=[DataRequired()])
    submit = SubmitField(Language()["Submit"])

class CommentForm(FlaskForm):
    body = TextAreaField(Language()["Body"], validators=[DataRequired()])
    submit = SubmitField(Language()["Submit"])
    subscribe = SubmitField(Language()["Subscribe"])
    unsubscribe = SubmitField(Language()["Unsubscribe"])

class GroupForm(FlaskForm):
    submit = SubmitField(Language()["New member"])
