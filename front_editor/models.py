import math

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.models import Page
from wagtail.search.backends import get_search_backend

from .post import Post
from .utils import is_in_group, user_has_perms


class PostsPage(RoutablePageMixin, Page):
    page_size = 10 # posts per page
    post_payload_limit = 5 # maximum size (MB) for each post

    @path("")
    @path("page/<int:page_num>/")
    @path("with/<int:post_id>/")
    def post_index(self, request, page_num=None, post_id=None):
        posts = self.posts.filter(live=True).order_by('-first_published_at')
        q = request.GET.get("q", '')
        if q:
            s = get_search_backend()
            posts = s.search(q, posts)
        paginator = Paginator(posts, self.page_size)
        if post_id:
            idx = None
            try:
                id_list = list(posts.values_list('id', flat=True))
                idx = id_list.index(post_id)
            except:
                try:
                    post_id = posts.filter(id__gt=post_id).last().id
                    idx = id_list.index(post_id)
                except:
                    pass
            if idx:
                page_num = math.ceil((id_list.index(post_id) + 1)/ self.page_size)

        if not page_num: 
            page_num = 1
        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context={
            "posts": posts,
            "paginator": paginator,
            "with_id": post_id,
            "filter": q,
            "q": f'?q={q}' if q else ''
        }
        if posts.has_other_pages():
            context['page_list'] = list(paginator.get_elided_page_range(posts.number, on_each_side=3, on_ends=2))

        return self.render(
            request,
            context_overrides=context,
            template="posts/post-list.html",
        )
    
    @path("new/")
    @path("<int:id>/edit/")
    @method_decorator(login_required, name='post_form')
    def post_form(self, request, id=None):
        from .forms import PostForm
        if not user_has_perms(request.user, Post, ['add', 'change', 'publish']):
            return HttpResponseForbidden("You do not have permission to access this page.")
        post = self.posts.filter(id=id).first() if id else None
        if id and not post:
            return HttpResponseNotFound()
        if post and (request.user != post.author and not is_in_group(request.user, "Post Moderators")):
            return HttpResponseForbidden("You do not have permission to access this page.")
        try:
            form = PostForm(request.POST or None, instance=post)
            if request.method == 'POST' and form.is_valid():
                # save instance revision and publish, don't use form.save method directly
                if form.instance.id:
                    form.instance.title = form.cleaned_data['title']
                    form.instance.content = form.cleaned_data['content']
                else:
                    form.instance.author = request.user
                    form.instance.page = self
                    form.instance.save()
                form.instance.save_revision().publish(user=request.user)
                return redirect(f'{self.url}with/{form.instance.id}/') 
        except Exception as e:
            print(e)

        return self.render(
            request, 
            template="posts/post-form.html", 
            context_overrides={
                'page': self,
                'form': form,
                'post': post
            }
        )

    @path("<int:id>/delete/")
    @method_decorator(login_required, name='delete_post')
    def delete_post(self, request, id):
        from .forms import PostForm
        if not user_has_perms(request.user, Post, ['delete']):
            return HttpResponseForbidden("You do not have permission to access this page.")
        post = Post.objects.filter(id=id).first() if id else None
        if not post:
            return HttpResponseNotFound()
        if post and (request.user != post.author and not is_in_group(request.user, "Post Moderators")):
            return HttpResponseForbidden("You do not have permission to access this page.")
        if request.method == 'POST' and post:
            form = PostForm(request.POST or None)
            if form.data['confirm'] == 'true':
                post.delete()
                return redirect(f'{self.url}with/{id}/') 
            
        return self.render(
            request, 
            template="posts/post-delete.html", 
            context_overrides={
                'page': self,
                'post': post
            }
        )
