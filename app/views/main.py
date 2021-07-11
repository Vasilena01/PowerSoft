from flask import (
    Blueprint,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    make_response,
    escape,
    jsonify,
    session,
)
from flask_security import current_user
from flask_mail import Message
from app.extensions import mail, db
from app.forms import SendEmailForm
from app.models import BlogPost, User
from app.helpers import prepare_json, conf, log
from app import create_app

main = Blueprint('main', __name__, url_prefix='/')


@main.route('')
def home():
    context = {
    }
    return render_template('main/home.html', **context)


@main.route('za-nas/')
def about():
    return render_template('main/about.html')


@main.route('kontakti/', methods=['GET', 'POST'])
def contacts():
    form = SendEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message(
                form.subject.data,
                sender=(escape(form.name.data), escape(form.email.data)),
                recipients=[conf('mail_form', 'recipient')]
            )
            msg.body = form.message.data
            mail.send(msg)
            flash(conf('msg', 'send_msg'), 'success')
            return redirect(url_for('main.contacts'))
        else:
            flash(conf('msg', 'send_msg_fail'), 'error')

    context = {
        'form': form,
    }
    return render_template('main/contacts.html', **context)


@main.route('usloviq/')
def terms():
    return render_template('main/terms.html')


@main.route('politika-za-poveritelnost/')
def privacy_policy():
    return render_template('main/privacy_policy.html')


@main.route('accept-cookies/', methods=['POST'])
def accept_cookies():
    session['has_accepted_cookies'] = True
    return jsonify(prepare_json('success'))


# Route for ajax use to get flashes
@main.route('get-flash/')
def get_flashes():
    return render_template('_messages.html')


# Custom errorhandlers
@main.errorhandler(404)
def not_found(e):
    """Page not found."""
    context = {
        'msg': 'Опа... Тази страница не може да бъде намерена',
        'info': 'Може би е била преместена или някой програмист е оплескал нещо',
    }
    return make_response(render_template('error.html', **context), 404)


@main.errorhandler(403)
def permission_denied(e):
    """Permission denied."""
    if current_user.is_anonymous:
        return redirect(url_for('security.login', next=request.url))
    flash(*conf('security', 'msg_unauthorized'))
    return redirect('/')


@main.errorhandler(400)
def bad_request(e):
    """Bad request."""
    context = {
        'msg': 'Някой програмист явно е оплескал нещо...',
        'info': 'Е, случва се и най-добрите :)',
    }
    return make_response(render_template('error.html', **context), 400)


@main.errorhandler(500)
def server_error(e):
    """Internal server error."""
    context = {
        'msg': 'Някой програмист явно е оплескал нещо...',
        'info': 'Е, случва се и най-добрите :)',
    }
    return make_response(render_template('error.html', **context), 500)

