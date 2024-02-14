from django.shortcuts import render, redirect
from .models import Post,BlogComments
from django.contrib import messages

# Create your views here.
def blogHome(request): 
    allPost = Post.objects.all()
    context = {'allPost':allPost}
    return render(request,'blog/blogHome.html',context)

def blogPost(request, slug): 
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments= BlogComments.objects.filter(post=post, parent=None)
    replies= BlogComments.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)
    context = {'post':post,'comments':comments,'replyDict': replyDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request): 
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        parentSno = request.POST.get('parentSno')
        post = Post.objects.get(sno = postSno)
        if parentSno == "":
            comment = BlogComments(comment = comment,user = user,post = post) 
            comment.save() 
            messages.success(request,"your comment posted succeed...")
        else:
            parent = BlogComments.objects.get(id = parentSno)
            comment = BlogComments(comment = comment,user = user,post = post,parent=parent) 
            comment.save() 
            messages.success(request,"your reply posted succeed...")
    return redirect(f'/blog/{post.slug}')