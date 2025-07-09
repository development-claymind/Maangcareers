from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from websiteManagement.serializers import TestimonialSerializer, MentorSerializer, FAQSerializer, BlogSerializer, BlogListSerializer
from websiteManagement.models import Testimonial, Mentor, FAQ, Blog


class TestimonialViewSet(ViewSet):

    def list(self, request):
        queryset = Testimonial.objects.order_by('pk')
        serializer = TestimonialSerializer(queryset, many=True)
        return Response(serializer.data)

class MentorViewSet(ViewSet):

    def list(self, request):
        queryset = Mentor.objects.order_by('pk')
        serializer = MentorSerializer(queryset, many=True)
        return Response(serializer.data)

class FAQViewSet(ViewSet):

    def list(self, request):
        queryset = FAQ.objects.order_by('pk')
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)

class BlogViewSet(ViewSet):

    def list(self, request):
        queryset = Blog.objects.order_by('pk')
        serializer = BlogListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Blog.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.views += 1
        item.save()
        serializer = BlogSerializer(item)
        return Response(serializer.data)