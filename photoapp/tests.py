from django.test import TestCase
from .models import Image

# Create your tests here.
class ImageTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.image=Image( image ='http://image.com/image.jpg',name= 'Nature', caption ='Our work to conserve biodiversity focuses on Key Biodiversity Areas.',comments='2',likes_counter=2,likes=2)


    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image))   

    def test_save_method(self):
        self.image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.image.save_image()
        self.image.delete_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 0)

    def tearDown(self):
        Image.objects.all().delete()

