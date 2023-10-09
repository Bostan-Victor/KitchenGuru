from django.test import TestCase
from gallery import models
from django.core.files import File

# Create your tests here.
class GalleryModelTest(TestCase):
    
    def test_gallery_model_save_and_retrieve(self):
        image1 = models.Image(title = 'Profile picture:', image = File(open('gallery/testimage1.jpg', 'rb')))
        image1.save()
        
        image2 = models.Image(title = 'Last profile picture', image = File(open('gallery/testimage1.jpg', 'rb')))
        image2.save()
        
        all_images = models.Image.objects.all()
        
        self.assertEqual(len(all_images), 2)
        
        self.assertEqual(all_images[0].title, image1.title)
        self.assertEqual(all_images[0].image, image1.image)
        
        self.assertEqual(all_images[1].title, image2.title) 
        self.assertEqual(all_images[1].image, image2.image)
