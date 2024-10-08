from flask import request, current_app, flash
from flask_mail import Message
from .extensions import db, mail
from transliterate import slugify
from ftplib import FTP, error_perm, all_errors
from PIL import Image
from datetime import datetime
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import inspect
import json
import uuid
import io
import os
import re


def prepare_json(status='fail', msg='', data={}):
    return {'status': status, 'msg': msg, 'data': data}


def generate_slug(string):
    slug = slugify(string)
    # slugify returns None if the strings doesn't contain non-english words for some reason
    if slug is None:
        slug = re.sub(r'[^1-9a-z ]', '', string.lower())
        slug = slug.replace(' ', '-')
    return slug


def optimize_image(file, size=(), max_size=None):
    img = Image.open(file)
    if size:
        img = img.convert('RGB')
        img.thumbnail(size, Image.LANCZOS)
    elif max_size:
        img = img.convert('RGB')
        size = img.size;
        # If width is bigger than height then using the max width
        # and else using the max height
        if size[0] > size[1]:
            width = max_size
            height = max_size * size[1] / size[0]
        else:
            height = max_size
            width = max_size * size[0] / size[1]
        img.thumbnail((width, height), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', optimize=True, quality=80)
    buf.seek(0)  # returning to the first byte of the file
    return buf


def _uuid():
    return str(uuid.uuid4().hex)


def get_ip():
    return request.remote_addr


def get_ftp_obj(address, username, password):
    ftp = FTP(address)
    ftp.login(user=username, passwd=password)
    return ftp


def get_cdn_ftp_obj():
    ftp = get_ftp_obj(
        conf('cdn', 'ftp_address'),
        conf('cdn', 'ftp_username'),
        conf('cdn', 'ftp_password'),
    )
    return ftp


def ftp_cd(ftp, directory):
    dirs = directory.split('/')
    try:
        dirs.remove('')
    except ValueError:
        pass

    for d in dirs:
        try:
            ftp.cwd(d)
        except error_perm:
            ftp.mkd(d)
            ftp.cwd(d)


def ftp_upload(ftp, file, filename, directory):
    try:
        ftp.cwd('/')
        ftp_cd(ftp, directory)
        ftp.storbinary('STOR '+filename, file)
    except all_errors as e:
        mail_log_error('Failed cdn ftp upload', f'Could not upload {directory + filename}\nError:\n{e}', get_caller_stack=True)


def ftp_delete(ftp, filename, directory):
    try:
        ftp.cwd(directory)
        ftp.delete(filename)
        return True
    except all_errors as e:
        mail_log_error('Failed cdn ftp delete', f'Could not remove {directory + filename}\nError:\n{e}', get_caller_stack=True)
        return False


def ftp_rmdr(ftp, path):
    # Recursively delete a directory tree on a remote server
    try:
        names = ftp.nlst(path)
        ftp.cwd(path)
    except all_errors as e:
        # some FTP servers complain when you try and list non-existent paths
        mail_log_error('Failed cdn ftp rmdr', f'Could not remove {path}\nError:\n{e}', get_caller_stack=True)
        return

    for name in names:
        if os.path.split(name)[1] in ('.', '..'):
            continue

        try:
            ftp.cwd(name)
            ftp.cwd('..')
            ftp_rmdr(ftp, name)
        except all_errors:
            ftp.delete(name)

    try:
        ftp.rmd(path)
    except all_errors as e:
        mail_log_error('Failed cdn ftp rmdr', f'Could not remove {path}\nError:\n{e}', get_caller_stack=True)
        return False


def ceildiv(a, b):
    return -(-a // b)


def mail_log_error(subject, body, get_caller_stack=False):
    # Getting the info of the caller (aka the outer frame)
    stack_index = 2 if get_caller_stack else 1  # Or the caller of the caller if needed
    frame, filename, line_number, function_name, lines, index = inspect.stack()[stack_index]
    stack = f'DateTime: {datetime.now()}\nFilename: {filename}\nLine: {line_number}\nFunction: {function_name}\n-------------------------------\n'
    body = stack + body

    if conf('debug'):
        log(f'{subject}\n{body}')
        return

    msg = Message(
        subject,
        sender=('PowerSoft', 'v.stanoyska@gmail.com'),
        recipients=[conf('errors_mail')]
    )
    msg.body = body
    mail.send(msg)


def conf(category, name=''):
    # Only returning from the config file because there is no settings table
    return current_app.config.get(f'{category}_{name}'.upper())

    if not name:
        full_name = category.upper()
    else:
        full_name = f'{category}_{name}'.upper()

    if not full_name in current_app.config:
        from .models import Setting  # Importing here as a workround of the circular import
        setting = Setting.query.filter_by(name=category).first()
        if not setting:
            mail_log_error('Undefined setting', f'Category: {category}\nName: {name}', get_caller_stack=True)
            return False

        found_conf = False
        data = json.loads(setting.data)  # NOTE kogato si napravq az formata za settings tova nqma da e nujno
        for _name, value in data.items():
            _full_name = f'{category}_{_name}'.upper()
            current_app.config[_full_name] = value
            if full_name == _full_name:
                found_conf = True

        if not found_conf:
            mail_log_error('Failed to find config setting', f'Category: {category}\nName: {name}', get_caller_stack=True)
            return False

    return current_app.config.get(full_name)


def log(msg, level='debug'):
    levels = {
        'debug': DEBUG,
        'info': INFO,
        'warning': WARNING,
        'error': ERROR,
        'critical': CRITICAL,
    }
    current_app.logger.log(levels.get(level, DEBUG), msg, stacklevel=2)

