from flask import request
from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField
from wtforms import (
    BooleanField,
    IntegerField,
    TextField,
    TextAreaField,
    SelectField,
    SelectMultipleField,
    FieldList,
    FormField,
)
from wtforms.fields.html5 import (
    SearchField,
    EmailField,
    TelField,
    DateField,
    DateTimeLocalField,
    DecimalField,
)
from wtforms.validators import Length, Email, InputRequired, DataRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_security.forms import ConfirmRegisterForm


# ---------- Mixins ----------
class MailFieldMixin:
    email = EmailField('Имейл', [
        Length(min=6, max=50, message='Невалиден имейл адрес'),
        InputRequired(message='Моля въведи своят имейл адрес'),
        Email(message='Имейлът изглежда не е валиден')
    ])


class NameFieldMixin:
    name = TextField('Име', [
        Length(max=50, message='Името ти не е ли малко дълго :)'),
        InputRequired(message='Моля въведи име')
    ])


class AgreementMixin:
    agreement = BooleanField('Съгласен съм с <a href="/politika-za-poveritelnost/">политиката за поверителност на лични данни</a>', [InputRequired(message='Няма как да продължиш напред без това съгласие.')])


class TitleMixin:
    title = TextField('Title', [InputRequired(message='Please provide a title')])


class OverviewMixin:
    overview = TextAreaField('Overview', [
        InputRequired(message=u'Please provide an overview')
    ])


class SlugMixin:
    slug = TextField('Slug (optional)')


# ---------- Forms ----------
class SignupFormExtension(NameFieldMixin, ConfirmRegisterForm, AgreementMixin):
    pass


class SendEmailForm(NameFieldMixin, MailFieldMixin, AgreementMixin, Form):
    subject = TextField('Тема', [
        InputRequired(message='Моля въведи тема')
    ])
    message = TextAreaField('Съобщение', [
        Length(max=10000),
        InputRequired(message='Моля въведи съобщение')
    ])


class BlogPostForm(TitleMixin, OverviewMixin, SlugMixin, Form):
    thumbnail = FileField('Select Thumbnail...')
    category = SelectField('Category', coerce=int)
    tags = TextField('Tags (separated by [, ])', [
        InputRequired(message=u'Please provide one or more tags')
    ])
    draft = BooleanField('Draft')
    content = TextAreaField('Post Content...')


class SearchForm(Form):
    q = SearchField('Търсене', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

