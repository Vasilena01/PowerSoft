from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask_security import login_required, roles_accepted, current_user
from flask_mail import Message
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask_admin.menu import MenuLink
from flask_admin.base import expose, BaseView
from flask_wtf import Form
from werkzeug.utils import secure_filename
from jinja2 import Markup

from app.extensions import db, admin, mail
from app.forms import (
    BlogPostForm,
    #SettingsForm,
)
from app.models import (
    #Setting,
    User,
    Role,
    BlogCategory,
    BlogPost,
)
from app.helpers import (
    prepare_json,
    generate_slug,
    optimize_image,
    get_cdn_ftp_obj,
    ftp_upload,
    ftp_delete,
    ftp_rmdr,
    _uuid,
    log,
    conf,
)

from datetime import datetime, date
import subprocess
import json
import os
import re
import io

admin_extension = Blueprint('admin_extension', __name__, url_prefix='/admin/')  # , template_folder='admin'


# ---------- Setting Up Flask Admin --------------

# Creating a custom formatter for datetime objects
def _date_formatter(view, value):
    return value.strftime('%d.%m. %Y')


# Adding custom formatters to defaults
CUSTOM_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
CUSTOM_FORMATTERS.update({
    date: _date_formatter
})

def _email_formatter(view, context, model, name):
    return Markup(f'<a href="mailto:{model.email}" target="_blank">{model.email}</a>')

def _tel_formatter(view, context, model, name):
    return Markup(f'<a href="tel:{model.tel}" target="_blank">{model.tel}</a>')

def _status_formatter(view, context, model, name):
    return model.statuses[model.status]



# Protecting Admin Base Views (for admins) (used for the admin home page)
class AdminBaseView(BaseView):
    def is_accessible(self):
        return (
            current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash(*conf('security_msg', 'unauthorized'))
                return redirect('/')
            else:
                return redirect(url_for('security.login', next=request.url))


# Protecting Admin Views (for admins)
class AdminModelView(ModelView):
    form_base_class = Form # Fix for the bad request error

    def is_accessible(self):
        return (
            current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash(*conf('security_msg', 'unauthorized'))
                return redirect('/')
            else:
                return redirect(url_for('security.login', next=request.url))


# Protecting Admin Views (for superusers)
class SuperuserModelView(ModelView):
    form_base_class = Form # Fix for the bad request error

    def is_accessible(self):
        return (
            current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash(*conf('security_msg', 'unauthorized'))
                return redirect('/')
            else:
                return redirect(url_for('security.login', next=request.url))


class StatsView(AdminBaseView):
    @expose('/')
    def stats(self):
        pass
        # return self.render('admin/stats.html', **context)


# ---------- Settings ----------
"""
class SettingAdmin(SuperuserModelView):
    form = SettingsForm
    column_searchable_list = ['name', 'data']
    column_filters = ['name']
    column_list = ['id', 'name']
    column_default_sort = ('id', False)
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_set_page_size = True
"""


# ---------- User Administration ----------
class UserAdmin(SuperuserModelView):
    form_excluded_columns = ['password', 'fs_uniquifier']
    column_exclude_list = ['password', 'fs_uniquifier']
    column_list = ['id', 'name', 'email', 'active', 'confirmed_at']
    column_searchable_list = ['name', 'email']
    column_filters = ['active']
    column_editable_list = ['name', 'active']
    column_default_sort = ('id', False)
    edit_modal = True
    can_create = False
    can_set_page_size = True


class RoleAdmin(SuperuserModelView):
    column_filters = ['name']
    column_editable_list = ['description']
    column_list = ['id', 'name', 'description']
    column_default_sort = ('id', False)
    can_edit = False
    edit_modal = True
    can_set_page_size = True


# ---------- Blog Admin ----------
class BlogCategoryAdmin(AdminModelView):
    column_searchable_list = ['name']
    column_editable_list = ['name']
    column_list = ['id', 'name']
    column_default_sort = ('name', False)
    create_modal = True
    can_edit = False
    can_set_page_size = True



class BlogPostAdmin(AdminModelView):
    column_type_formatters = CUSTOM_FORMATTERS
    column_exclude_list = ['overview', 'thumbnail', 'content']
    column_list = ['id', 'category', 'title', 'views', 'draft', 'date']
    column_searchable_list = ['category.name', 'title']
    column_filters = ['draft', 'category.name']
    column_editable_list = ['draft', 'category']
    column_default_sort = ('date', True)
    can_set_page_size = True

    def _title_formatter(view, context, model, name):
        return Markup(f'<a href="{url_for("blog.post", id=model.id, slug=model.slug)}" target="_blank">{model.title}</a>')

    column_formatters = {
        'title': _title_formatter
    }

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        categories = BlogCategory.query.all()
        categories_list = [(i.id, i.name) for i in categories]

        form = BlogPostForm()
        form.category.choices = categories_list

        if form.validate_on_submit():
            # Adding the post into the db
            new_post = BlogPost(
                title=form.title.data,
                slug=form.slug.data if form.slug.data else generate_slug(form.title.data),
                overview=form.overview.data,
                content=form.content.data,
                category_id=form.category.data,
                tags=form.tags.data,
                draft=True if form.draft.data else False
            )
            db.session.add(new_post)
            db.session.commit()

            # Optimizing the thumbnail
            thumbnail = form.thumbnail.data
            og_filename = os.path.splitext(secure_filename(thumbnail.filename))
            filename = f'{og_filename[0]}_{new_post.id}_thumbnail.jpg'
            thumbnail = optimize_image(thumbnail, size=conf('blog', 'thumbnail_size'))

            # Uploading the thumbnail to the cdn
            ftp = get_cdn_ftp_obj()
            ftp_upload(ftp, thumbnail, filename, conf('cdn', 'ftp_dir_blog'))
            ftp.quit()

            # Updating the thumbnail name in the db
            new_post.thumbnail = filename
            db.session.commit()
            if request.form.get('create_add_another'):
                return redirect(url_for('blog_posts.create_view'))
            else:
                return redirect(url_for('blog_posts.index_view'))
        elif request.method == 'POST':
            flash('Validation failed, please check if all the data is filled in', 'error')

        context = {
            'form': form,
            'action': 'create',
        }
        return self.render('admin/blog_post_form.html', **context)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        categories = BlogCategory.query.all()
        categories_list = [(i.id, i.name) for i in categories]

        form = BlogPostForm()
        form.category.choices = categories_list

        id = request.args.get('id', default=None, type=int)

        post = BlogPost.query.get_or_404(id)
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data if form.slug.data else generate_slug(form.title.data),
            post.overview = form.overview.data
            post.category_id = form.category.data
            post.tags = form.tags.data
            post.draft = True if form.draft.data else False
            post.content = form.content.data

            if form.thumbnail.data:
                thumbnail = form.thumbnail.data
                og_filename = os.path.splitext(secure_filename(thumbnail.filename))
                filename = f'{og_filename[0]}_{id}_thumbnail.jpg'
                thumbnail = optimize_image(thumbnail, size=conf('blog', 'thumbnail_size'))

                ftp = get_cdn_ftp_obj()
                ftp_upload(ftp, thumbnail, filename, conf('cdn', 'ftp_dir_blog'))
                ftp_delete(ftp, post.thumbnail, conf('cdn', 'ftp_dir_blog'))
                ftp.quit()
                post.thumbnail = filename

            db.session.commit()
            flash('Saved changes successfully', 'success')
            return redirect(url_for('blog_posts.edit_view', id=id))
        elif request.method == 'POST':
            flash('Validation failed, please check if all the data is filled in', 'error')

        form = BlogPostForm(title=post.title,
                        slug=post.slug,
                        overview=post.overview,
                        category=post.category_id,
                        tags=post.tags,
                        content=post.content,
                        draft=post.draft)
        form.category.choices = categories_list

        context = {
            'form': form,
            'action': 'edit',
            'post': post,
        }
        return self.render('admin/blog_post_form.html', **context)


# ---------- Registering Flask-Admin views ----------
admin.add_view(UserAdmin(User, db.session, name='Users', category='User Management', url='users'))
admin.add_view(RoleAdmin(Role, db.session, name='Roles', category='User Management', url='users-roles'))

admin.add_view(BlogPostAdmin(BlogPost, db.session, name='Posts', category='Blog', endpoint='blog_posts', url='blog-posts'))
admin.add_view(BlogCategoryAdmin(BlogCategory, db.session, name='Categories', category='Blog', endpoint='blog_categories', url='blog-categories'))

#admin.add_view(SettingAdmin(Setting, db.session, name='Settings', endpoint='settings'))


# Adding a back to public website link
admin.add_link(MenuLink(name='Public Website', category='', url='/'))


# ---------- Adding Custom Routes to Admin --------------
@admin_extension.route('posts/add-category/', methods=['POST'])
@roles_accepted('admin')
def add_post_category():
    name = request.get_json()['name']
    new_category = BlogCategory(name=name)
    db.session.add(new_category)
    db.session.commit()
    response = prepare_json('success', 'Category added successfully', {'id': new_category.id})
    return jsonify(response)


@admin_extension.route('posts/upload-image/', methods=['POST'])
@roles_accepted('admin')
def upload_post_image():
    image = request.files['file']

    og_filename = os.path.splitext(secure_filename(image.filename))
    filename = f'{og_filename[0]}_{_uuid()}.jpg'
    image = optimize_image(image, size=conf('blog', 'thumbnail_size'))

    ftp = get_cdn_ftp_obj()
    ftp_upload(ftp, image, filename, conf('cdn', 'ftp_dir_blog'))
    ftp.quit()

    response = prepare_json(
        'success',
        'Image uploaded successfully',
        {'url': f'{conf("cdn", "url")}{conf("cdn", "dir_blog")}{filename}'}
    )
    return jsonify(response)


@admin_extension.route('posts/delete-image/', methods=['POST'])
@roles_accepted('admin')
def delete_post_image():
    file_src = request.get_json()['src']
    filename = file_src.split('/')[-1]
    ftp = get_cdn_ftp_obj()

    if not ftp_delete(ftp, filename, conf('cdn', 'ftp_dir_blog')):
        response = prepare_json('fail', 'Image could not be removed')
    else:
        response = prepare_json('success', 'Image removed successfully')
    ftp.quit()

    return jsonify(response)

