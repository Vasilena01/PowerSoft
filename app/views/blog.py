from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
)
from flask_security import current_user
from app.models import BlogPost, BlogCategory
from app.extensions import db
from app.forms import SearchForm
from app.helpers import log, conf
from datetime import datetime

blog = Blueprint('blog', __name__, url_prefix='/blog/')


@blog.route('')
def index():
    search_form = SearchForm()
    page = request.args.get('page', type=int, default=1)

    if search_form.validate():
        q = search_form.q.data
        query = BlogPost.search(q)
        posts = query.filter_by(draft=False).paginate(page, per_page=conf('blog', 'posts_per_page'))
    else:
        # Removing draft filter if admin so admins can preview posts before they are published
        if current_user.has_role('admin'):
            posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page, per_page=conf('blog', 'posts_per_page'))
        else:
            posts = BlogPost.query.filter_by(draft=False).order_by(BlogPost.date.desc()).paginate(page, per_page=conf('blog', 'posts_per_page'))
        search_form = SearchForm(q='')
        q = False

    categories = BlogCategory.query.order_by(BlogCategory.name.asc()).all()
    context = {
        'posts': posts,
        'categories': categories,
        'search_form': search_form,
        'q': q,
    }
    return render_template('blog/blog.html', **context)


@blog.route('<category_slug>-<int:category_id>/')
def filter_by_category(category_slug, category_id):
    search_form = SearchForm()
    page = request.args.get('page', type=int, default=1)

    if category_id == 0:
        category = 'най-популярни';
        posts = BlogPost.query.filter_by(draft=False) \
                .order_by(BlogPost.views.desc()) \
                .paginate(page, per_page=conf('blog', 'posts_per_page'))
    else:
        category = BlogCategory.query.get_or_404(category_id)
        posts = BlogPost.query.filter_by(draft=False, category=category) \
                .order_by(BlogPost.date.desc()) \
                .paginate(page, per_page=conf('blog', 'posts_per_page'))

    if not posts:
        abort(404)

    categories = BlogCategory.query.all()

    context = {
        'posts': posts,
        'categories': categories,
        'category_id': category_id,
        'category': category,
        'search_form': search_form,
    }
    return render_template('blog/blog.html', **context)


@blog.route('<int:id>-<slug>/')
def post(id, slug):
    post = BlogPost.query.get_or_404(id)

    if post.draft and not current_user.has_role('admin'):
        return redirect(url_for('pages.home'))

    more = BlogPost.query.filter(BlogPost.draft != True, BlogPost.category_id == post.category.id, BlogPost.id != post.id) \
            .order_by(BlogPost.date.desc()).limit(6).all()
    latest = BlogPost.query.filter(BlogPost.draft != True, BlogPost.id != post.id).order_by(BlogPost.date.desc()).limit(6).all()
    most_popular = BlogPost.query.filter(BlogPost.draft != True, BlogPost.id != post.id).order_by(BlogPost.views.desc()).limit(6).all()

    if 'viewed_posts' not in session:
        session['viewed_posts'] = []
    if id not in session['viewed_posts']:
        session['viewed_posts'].append(id)
        post.views += 1
        db.session.commit()

    context = {
        'post': post,
        'more': more,
        'latest': latest,
        'most_popular': most_popular,
    }
    return render_template('blog/post.html', **context)


# Makes big nums easily readable
@blog.app_template_filter()
def big_num(num):
    if num < 1000:
        return num
    elif num < 10000:
        return f'{round(num/1000, 1)}K'
    elif num < 1000000:
        return f'{num//1000}K'
    elif num < 10000000:
        return f'{round(num/1000000, 1)}M'
    elif num < 1000000000:
        return f'{num//1000000}M'
    elif num < 10000000000:
        return f'{round(num/1000000000, 1)}B'
    else:
        return f'{num//1000000000}B'

