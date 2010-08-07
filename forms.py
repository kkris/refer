#!/usr/bin/env python

from flaskext.wtf import Form, TextField, PasswordField, TextAreaField, \
                            HiddenField, Required
from flaskext.wtf import validators

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

class PostForm(Form):
    title = TextField('title', validators=[Required()])
    post = TextAreaField('post', validators=[Required()])
    tags = TextField('tags', validators=[Required()])

class CommentForm(Form):
    author = TextField('name', validators=[Required()])
    email = TextField('email (not visible to others)', 
                        validators=[Required(), validators.email()])
    comment = TextAreaField('comment', 
                            validators=[Required(), validators.Length(2, 500)])
