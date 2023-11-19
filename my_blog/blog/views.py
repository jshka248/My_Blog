from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView
from .models import Post, Comment, Reply, Tag
from .forms import PostForm, CommentForm, ReplyForm
from django.urls import reverse_lazy
from django.shortcuts import render

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(tags__name__icontains=q)).distinct()
        return qs

post_list = PostListView.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        post = form.save(commit=False)
        post.save()
        video = form.save(commit=True)
        video.user = self.request.user
        tag_names = form.cleaned_data['tags']
        if tag_names:  
            for tag_name in tag_names.split(','):
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)

        return super().form_valid(form)

post_new = PostCreateView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['replies'] = Reply.objects.filter(post=self.object).order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['reply_form'] = ReplyForm()
        return context
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)

post_detail = PostDetailView.as_view()


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/form.html'

    def test_func(self): # UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩, True, False 값으로 접근 제한
        return self.get_object().user == self.request.user

post_edit = PostUpdateView.as_view()


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        return get_object_or_404(Post, id=post.id)

post_delete = PostDeleteView.as_view()


# 댓글 생성 뷰
class CommentNewView(LoginRequiredMixin, CreateView):
    # POST 요청 처리
    def post(self, request, pk):
        # 요청받은 pk로 Post 객체를 가져옴. 없으면 404 에러 반환
        post = get_object_or_404(Post, pk=pk)
        # POST 데이터를 이용해 CommentForm 인스턴스를 생성
        form = CommentForm(request.POST)
        # 폼의 유효성 검사
        if form.is_valid():
            # 폼 데이터로 Comment 인스턴스를 생성하지만 DB에는 저장하지 않음
            comment = form.save(commit=False)
            # Comment 인스턴스의 post 필드 설정
            comment.post = post
            # Comment 인스턴스의 user 필드 설정
            comment.user = request.user
            # Comment 인스턴스를 DB에 저장
            comment.save()
            # 저장 후 블로그 상세 페이지로 리다이렉트
            return redirect('blog:post_detail', pk)
        # 유효하지 않은 폼을 사용자에게 다시 보여줌
        return render(request, 'blog/form.html', {'form': form})

    # GET 요청 처리
    def get(self, request):
        # 빈 CommentForm 인스턴스를 생성
        form = CommentForm()
        # 폼을 사용자에게 보여줌
        return render(request, 'blog/form.html', {'form': form})

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
comment_new = CommentNewView.as_view()


# 댓글 수정 뷰
class CommentUpdateView(UserPassesTestMixin, UpdateView):
    # Comment 모델을 기반으로 뷰를 생성
    model = Comment
    # 사용할 폼 클래스 지정
    form_class = CommentForm
    # 사용할 템플릿 이름 지정
    template_name = 'blog/form.html'

    # 요청된 객체를 가져오는 메서드. URL의 키워드 인자를 이용해 댓글을 찾음
    def get_object(self, queryset=None):
        return get_object_or_404(Comment, post__pk=self.kwargs['post_pk'], pk=self.kwargs['comment_pk'])

    # 수정 성공 후 리다이렉트할 URL을 반환하는 메서드
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # UserPassesTestMixin의 테스트 함수. 현재 요청한 사용자가 댓글의 작성자와 같은지 확인
    def test_func(self): 
        return self.get_object().user == self.request.user

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
comment_edit = CommentUpdateView.as_view()


# 댓글 삭제 뷰
class CommentDeleteView(UserPassesTestMixin, DeleteView):
    # Comment 모델을 기반으로 뷰를 생성
    model = Comment
    # 사용할 템플릿 이름 지정
    template_name = 'blog/post_confirm_delete.html'
    
    # 요청된 객체를 가져오는 메서드. URL의 키워드 인자를 이용해 댓글을 찾음
    def get_object(self, queryset=None):
        return get_object_or_404(Comment, post__pk=self.kwargs['post_pk'], pk=self.kwargs['comment_pk'])

    # 삭제 성공 후 리다이렉트할 URL을 반환하는 메서드
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # UserPassesTestMixin의 테스트 함수. 현재 요청한 사용자가 댓글의 작성자와 같은지 확인
    def test_func(self): 
        return self.get_object().user == self.request.user

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
comment_delete = CommentDeleteView.as_view()


# 댓글에 대한 답글 생성 뷰
class CommentReplyView(LoginRequiredMixin, CreateView):
    # POST 요청 처리
    def post(self, request, post_pk, comment_pk):
        # 요청받은 Post, Comment 모델 중 pk값이 post_pk, comment_pk 객체를 가져옴. 없으면 404 에러 반환
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        # POST 데이터를 이용해 ReplyForm 인스턴스를 생성
        form = ReplyForm(request.POST)
        # 폼의 유효성 검사
        if form.is_valid():
            # 폼 데이터로 Reply 인스턴스를 생성하지만 DB에는 저장하지 않음
            reply = form.save(commit=False)
            # Reply 인스턴스의 post, comment, user 필드 설정
            reply.post = post
            reply.comment = comment
            reply.user = request.user
            # Reply 인스턴스를 DB에 저장
            reply.save()
            # 저장 후 블로그 상세 페이지로 리다이렉트
            return redirect('blog:post_detail', post_pk)
        # 유효하지 않은 폼을 사용자에게 다시 보여줌
        return render(request, 'blog/form.html', {'form': form})

    # GET 요청 처리
    def get(self, request, post_pk, comment_pk):
        # 빈 ReplyForm 인스턴스를 생성
        form = ReplyForm()
        # 폼을 사용자에게 보여줌
        return render(request, 'blog/form.html', {'form': form, 'post_pk': post_pk, 'comment_pk': comment_pk})

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
comment_reply = CommentReplyView.as_view()


# 답글 수정 뷰
class ReplyUpdateView(UserPassesTestMixin, UpdateView):
    # Reply 모델을 기반으로 뷰를 생성
    model = Reply
    # 사용할 폼 클래스 지정
    form_class = ReplyForm
    # 사용할 템플릿 이름 지정
    template_name = 'blog/form.html'

    # 요청된 객체를 가져오는 메서드. URL의 키워드 인자를 이용해 답글을 찾음
    def get_object(self, queryset=None):
        return get_object_or_404(Reply, comment__post__pk=self.kwargs['post_pk'], comment__pk=self.kwargs['comment_pk'], pk=self.kwargs['reply_pk'])

    # 수정 성공 후 리다이렉트할 URL을 반환하는 메서드
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # UserPassesTestMixin의 테스트 함수. 현재 요청한 사용자가 답글의 작성자와 같은지 확인
    def test_func(self): 
        return self.get_object().user == self.request.user

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
reply_edit = ReplyUpdateView.as_view()


# 답글 삭제 뷰
class ReplyDeleteView(UserPassesTestMixin, DeleteView):
    # Reply 모델을 기반으로 뷰를 생성
    model = Reply
    # 사용할 템플릿 이름 지정
    template_name = 'blog/post_confirm_delete.html'

    # 요청된 객체를 가져오는 메서드. URL의 키워드 인자를 이용해 답글을 찾음
    def get_object(self, queryset=None):
        return get_object_or_404(Reply, comment__post__pk=self.kwargs['post_pk'], comment__pk=self.kwargs['comment_pk'], pk=self.kwargs['reply_pk'])

    # 삭제 성공 후 리다이렉트할 URL을 반환하는 메서드
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # UserPassesTestMixin의 테스트 함수. 현재 요청한 사용자가 답글의 작성자와 같은지 확인
    def test_func(self): 
        return self.get_object().user == self.request.user

# 뷰를 함수형 뷰로 변환하여 URLconf에서 사용할 수 있게 함
reply_delete = ReplyDeleteView.as_view()

