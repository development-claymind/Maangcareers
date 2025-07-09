from rest_framework.routers import SimpleRouter
from websiteManagement import views


router = SimpleRouter()

router.register(r'testimonials', views.TestimonialViewSet, 'Testimonial')
router.register(r'mentors', views.MentorViewSet, 'Mentor')
router.register(r'faqs', views.FAQViewSet, 'FAQ')
router.register(r'blogs', views.BlogViewSet, 'Blog')

urlpatterns = router.urls
