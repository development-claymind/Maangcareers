from rest_framework.serializers import ModelSerializer
from websiteManagement.models import Testimonial, Mentor, FAQ, Blog, Comment, BlogTopic


class TestimonialSerializer(ModelSerializer):

    class Meta:
        model = Testimonial
        fields = '__all__'


class MentorSerializer(ModelSerializer):

    class Meta:
        model = Mentor
        fields = '__all__'


class FAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class BlogListSerializer(ModelSerializer):

    class Meta:
        model = Blog
        # fields = (
        #     'id',
        #     'title',
        #     'photo',
        #     'date',
        #     'popular',
        #     'read_time',
        #     'count_comments',
        #     'views',
        # )
        fields = "__all__"
class BlogTopicSerialzer(ModelSerializer):
    class Meta:
        model = BlogTopic
        fields = '__all__'
class CommentSerialzer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
class BlogSerializer(ModelSerializer):

    comments = CommentSerialzer(many=True)
    topics = BlogTopicSerialzer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'
