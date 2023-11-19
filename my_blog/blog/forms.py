# Django에서 제공하는 forms 모듈을 가져옵니다. 이 모듈은 HTML form에 대응하는 Python 클래스를 제공합니다.
from django import forms
# 현재 디렉토리의 models.py 파일에서 Post, Comment, Tag, Reply 모델을 가져옵니다.
from .models import Post, Comment, Tag, Reply

# PostForm은 Post 모델에 대한 정보를 입력받는 HTML form에 대응하는 Python 클래스입니다.
class PostForm(forms.ModelForm):
    # 사용자로부터 태그 정보를 입력받는 필드를 추가합니다.
    tags = forms.CharField()

    # 내부 Meta 클래스는 이 폼이 어떤 모델과 관련이 있는지, 그리고 모델의 어떤 필드에 대응하는 입력을 받는지 Django에게 알려줍니다.
    class Meta:
        # 이 폼은 Post 모델과 관련이 있습니다.
        model = Post
        # Post 모델의 'title', 'content', 'thumb_image', 'file_upload', 'tags' 필드에 대응하는 입력을 받습니다.
        fields = ['title', 'content', 'thumb_image', 'file_upload', 'tags'] 

    # save 메소드는 사용자로부터 받은 입력을 바탕으로 Post 객체를 생성하고 데이터베이스에 저장합니다.
    def save(self, commit=True):
        # super().save(commit=False)는 Post 객체를 생성하지만 아직 데이터베이스에 저장하지는 않습니다.
        instance = super().save(commit=False)
        # 생성한 Post 객체를 데이터베이스에 저장합니다.
        instance.save()
        # 저장한 Post 객체를 반환합니다.
        return instance


# CommentForm은 Comment 모델에 대한 정보를 입력받는 HTML form에 대응하는 Python 클래스입니다.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


# TagForm은 Tag 모델에 대한 정보를 입력받는 HTML form에 대응하는 Python 클래스입니다.
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


# ReplyForm은 Reply 모델에 대한 정보를 입력받는 HTML form에 대응하는 Python 클래스입니다.
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message']