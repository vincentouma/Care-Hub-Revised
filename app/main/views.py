from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PostForm,SubscriberForm,CommentForm
from ..import db,photos
from ..models import User,Post,Role,Subscriber,Comment
from flask_login import login_required,current_user
import markdown2
from ..email import mail_message
# from ..request import get_quote

@main.route("/",methods=['GET','POST'])
def index():
    """
    View root page function that returns the index page and its data
    """
    posts = Post.query.all()
    form = SubscriberForm()
    if form.validate_on_submit():
        email = form.email.data

        new_subscriber=Subscriber(email=email)
        new_subscriber.save_subscriber()

        mail_message("Subscription Received","email/welcome_subscriber",new_subscriber.email,subscriber=new_subscriber)

    title = "Welcome to My Blog"

    # name  = "Quote"
    # quote = get_quote()

    return render_template('index.html',title=title,posts=posts,subscriber_form=form)#name=name,#quote=quote

#######*********************SURPORT**************************##############
####*********************************************************##############
@main.route("/support")
def support():
    """
    A view that displays the pattient support page

    """
    title = 'Support'
    return render_template("support.html", title = title)

#########*****************END SUPPORT**********************************#############
#######***************************************************************##############

########*********************PROVIDER*********************************#############
##########************************************************************#############
@main.route("/provider")
def provider():
    """
    A view that displays the pattient service provider(s) page

    """
    title = 'Providers'
    return render_template("provider.html", title = title)

#########***************** Services **********************************#############
#######***************************************************************##############
@main.route("/services")
def services():
    """
    A view that displays the pattient service provider(s) page

    """
    title = 'Providers'
    return render_template("services.html", title = title)

#########***************** FACTS **********************************#############
#######***************************************************************##############
#########***************** Services **********************************#############
#######***************************************************************##############
@main.route("/news")
def news():
    """
    A view that displays the pattient service provider(s) page

    """
    title = 'News'
    return render_template("news.html", title = title)

#########***************** FACTS **********************************#############
#######***************************************************************##############
@main.route("/fact")
def fact():
    """
    A view that displays the cancer facts page

    """
    title = 'Facts'
    return render_template("fact.html", title = title)

#########*****************END FACTS**********************************#############
#######***************************************************************##############


#########*****************ABOUT**********************************#############
#######***************************************************************##############
@main.route("/about")
def about():
    """
    A view that displays the information about the project

    """
    title = 'Facts'
    return render_template("about.html", title = title)

#########*****************END ABOUT**********************************#############
#######***************************************************************##############

############********************* CONTACT US *************************##############
################******************************************************##############
@main.route('/contact')
def contact():

    title = 'Contact Us'

    return render_template("contact.html")

############**************************END CONTACT US *******************###########
#################*****************************************************#############


############********************* CONTACT US *************************##############
################******************************************************##############
@main.route('/facts')
def facts():

    title = 'Contact Us'

    return render_template("facts.html")

############**************************END CONTACT US *******************###########
#################*****************************************************#############
############********************* BLOG *************************##############
################******************************************************##############
@main.route('/blog')
def blog():

    title = 'blog'

    return render_template("contact.html")

############**************************END CONTACT US *******************###########
#################*****************************************************#############

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route("/new_post",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        new_post=Post(title=title,post=post,category=category)

        new_post.save_post()

        subscribers=Subscriber.query.all()

        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_post",subscriber.email,post=new_post)

        return redirect(url_for('main.index'))

    title="Make a post"
    return render_template('new_post.html',title=title,post_form=form)

@main.route("/post/<int:id>",methods=['GET','POST'])
def post(id):
    post=Post.query.get_or_404(id)
    comment = Comment.query.all()
    form=CommentForm()

    if request.args.get("like"):
        post.like = post.like+1

        db.session.add(post)
        db.session.commit()

        return redirect("/post/{post_id}".format(post_id=post.id))

    if form.validate_on_submit():
        comment=form.comment.data
        new_comment = Comment(id=id,comment=comment,user_id=current_user.id,post_id=post.id)

        new_comment.save_comment()

        return redirect("/post/{post_id}".format(post_id=post.id))

    return render_template('post.html',post=post,comments=comment,comment_form=form)
