from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import PitchForm,CommentForm,UpvoteForm,DownvoteForm,UpdateProfile
from flask_login import login_required,current_user
from flask.views import View, MethodView
from ..model import User,Comment,Post
from ..import db,photos
from datetime import datetime
from ..request import get_quotes
import markdown2

@main.route('/')
def login():
    return redirect(url_for('auth.login'))

@main.route('/index')
def index():
    quote=get_quotes()
    print('*******quotedata*****')
    print(quote)

    allposts=Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html',allposts=allposts,quote=quote)

@main.route('/about')
def about():

    return render_template('about.html')

@main.route('/post/<int:post_id>')
#displays a specific post
def post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    date=post.date.strftime('%B %d, %Y')
    time=post.date.strftime('%I : %M %p')

    return render_template('post.html',post=post,date=date,time=time)

@main.route('/add' , methods=['POST','GET'])
def add():
    return render_template('add.html')

@main.route('/showpost',methods=['POST'])
def showpost():
    title=request.form['title']
    subtitle=request.form['subtitle']
    name=request.form['name']
    content=request.form['content']
    
    #creating an instance of post class
    postadded=Post(owner_id=current_user.id,title=title,subtitle=subtitle,name=name,content=content,date=datetime.now())

    #adding to the database
    db.session.add(postadded)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()
    commentslist=Comment.get_comments(current_user.id)

    if user is None:
        abort (404)

    return render_template("profile/userprofile.html",user=user,commentslist=commentslist)

@main.route('/user/<uname>/update', methods=['GET','POST'])
@login_required

def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort (404)

    form=UpdateProfile()

    if form.validate_on_submit():
        user.bio=form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/addcomment/<int:posts_id>',methods=['POST','GET'])
def addcomment(posts_id):

    posts=Post.query.get(posts_id)

    return render_template('comment.html',posts=posts)


@main.route('/comment/<int:posts_id>', methods = ['POST'])
@login_required
def configurecomment(posts_id):
    comment=request.form['comment']
    posts=Post.query.get(posts_id)
    newcomment=Comment(id=current_user.id,comment=comment,comment_date=datetime.now())

    db.session.add(newcomment)
    db.session.commit()

    return redirect(url_for('main.displaycomment'))

@main.route('/displaycomment', methods=['POST','GET'])
def displaycomment():
    
    all_comments=Comment.query.order_by(Comment.comment_date.desc()).all()

    return render_template('displaycomment.html',all_comments = all_comments)

@main.route('/deletecomment/<int:comments_id>')

def deletecomment(comments_id):

    # newcomment=Comment(id=id,posts_id=posts_id,user_id=user_id,comment=comment,comment_date=datetime.now())

    deletecom=Comment.query.filter_by(id=comments_id).first()
    
    db.session.delete(deletecom)
    db.session.commit()

    return render_template('displaycomment.html')
    
# @main.route('/updatepost/<int:posts_id>', methods=['GET','POST'])
# @login_required
# def updatepost(posts_id):


#     blog=Post.query.filter_by(id=posts_id).first()

#     title=request.form['title']
#     subtitle=request.form['subtitle']
#     content=request.form['name']
#     name=request.form['content']
    
#     db.session.add(blog)
#     db.session.commit()

#     return redirect(url_for('.index',posts_id=blog.id))

#     return render_template('profile/updatepost.html')


@main.route('/deletepost/<int:posts_id>')
def deletepost(posts_id):
    deleteitem=Post.query.filter_by(id=posts_id).first()
    
    db.session.delete(deleteitem)
    db.session.commit()

    return redirect(url_for('main.index'))


    
    
    
