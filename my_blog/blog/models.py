# Django의 기본 모듈과 사용자 모델, 그리고 RichTextField를 위한 ckeditor 모듈을 임포트합니다.
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# 게시글에 대한 모델을 정의합니다.
class Post(models.Model):
    # 게시글 작성자, User 모델을 참조하며, 사용자가 삭제되면 해당 사용자의 게시글도 함께 삭제됩니다.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    # 게시글의 제목, 최대 길이는 100자입니다.
    title = models.CharField(max_length=100)
    # 게시글의 내용입니다.
    content = models.TextField()
    # 게시글의 썸네일 이미지, 'blog/images/%Y/%m/%d/' 경로에 업로드됩니다. 선택적 필드입니다.
    thumb_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 게시글에 첨부할 파일, 'blog/files/%Y/%m/%d/' 경로에 업로드됩니다. 선택적 필드입니다.
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)
    # 게시글이 생성된 시각, 자동으로 현재 시각이 저장됩니다.
    created_at = models.DateTimeField(auto_now_add=True)
    # 게시글이 수정된 날짜, 자동으로 현재 날짜가 저장됩니다.
    updated_at = models.DateField(auto_now=True)
    # 게시글의 조회 수, 기본값은 0입니다.
    view_count = models.PositiveIntegerField(default=0)
    # 게시글의 태그, Tag 모델을 참조합니다. 선택적 필드입니다.
    tags = models.ManyToManyField('Tag', blank=True)

    # 게시글의 제목을 반환하는 메서드입니다.
    def __str__(self):
        return self.title
    
    # 게시글의 절대 URL을 반환하는 메서드입니다.
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
# 댓글에 대한 모델을 정의합니다.
class Comment(models.Model):
    # 댓글이 달린 게시글, Post 모델을 참조하며, 게시글이 삭제되면 해당 게시글의 댓글도 함께 삭제됩니다.
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    # 댓글 작성자, User 모델을 참조하며, 사용자가 삭제되면 해당 사용자의 댓글도 함께 삭제됩니다.
    user  = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    # 댓글의 내용입니다.
    message = models.TextField()
    # 댓글이 생성된 시각, 자동으로 현재 시각이 저장됩니다.
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글이 수정된 날짜, 자동으로 현재 날짜가 저장됩니다.
    updated_at = models.DateField(auto_now=True)
    # 댓글 내용에 대한 Rich Text입니다.
    content = RichTextField()
    
    # 댓글의 내용을 반환하는 메서드입니다.
    def __str__(self):
        return self.message
    
# 태그에 대한 모델을 정의합니다.
class Tag(models.Model):
    # 태그의 이름, 최대 길이는 50자이며, 중복은 허용되지 않습니다. 선택적 필드입니다.
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # 태그의 이름을 반환하는 메서드입니다.
    def __str__(self):
        return self.name
    
# 답글에 대한 모델을 정의합니다.
class Reply(models.Model):
    # 답글이 달린 게시글, Post 모델을 참조하며, 게시글이 삭제되면 해당 게시글의 답글도 함께 삭제됩니다.
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='reply'
    )
    # 답글이 달린 댓글, Comment 모델을 참조하며, 댓글이 삭제되면 해당 댓글의 답글도 함께 삭제됩니다.
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies'
    )
    # 답글 작성자, User 모델을 참조하며, 사용자가 삭제되면 해당 사용자의 답글도 함께 삭제됩니다.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    # 답글의 내용입니다.
    message = models.TextField()
    # 답글이 생성된 시각, 자동으로 현재 시각이 저장됩니다.
    created_at = models.DateTimeField(auto_now_add=True)
    # 답글이 수정된 날짜, 자동으로 현재 날짜가 저장됩니다.
    updated_at = models.DateField(auto_now=True)

    # 답글의 내용을 반환하는 메서드입니다.
    def __str__(self):
        return self.message
