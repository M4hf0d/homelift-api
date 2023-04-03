from django.db import models
from django.core.validators import MaxValueValidator,  MinValueValidator
from users.models import Customer







# Sort default image dirs of products by name
def upload_image_product_url(instance, filename):
    return f'products_app/api/images/{instance.name}-product/images/default-image/{filename}'


# Sort other images dirs of products
def upload_other_images_product_url(instance, filename):
    return f'products_app/api/images/other-images/{filename}'





class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'categories'
        verbose_name_plural = "Categories"



class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    categoryList = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subCategories')


    def __str__(self):
   
        return f'{self.categoryList.name} --> {self.name}'

    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "Sub Categories"




class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_image_product_url, null=True, blank=True)
    subcategory =models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,editable=False)
    price = models.FloatField(default=0,
                       validators=[MaxValueValidator(1000000000.00),MinValueValidator(0)])
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    rating_rv= models.FloatField(default=0)
    rating_nb= models.PositiveIntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # set the category field based on the related subcategory
        self.category = self.subcategory.categoryList

        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    
    productList = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='productImages')
    image = models.ImageField(upload_to=upload_other_images_product_url)
    class Meta:
        db_table = 'images'
    def save(self, *args, **kwargs):
        if not self.pk:  # if creating a new instance
            product = self.productList
            if not product.image:  # if product doesn't have an image yet
                product.image = self.image
                product.save()
        super().save(*args, **kwargs)    
    

class ProductRating(models.Model):
    rating_user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    productList = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productRatings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.productList.name+" rating's is "+str(self.rating)

    class Meta:
        db_table = 'rating'

class ProductComment(models.Model):
    comment_user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    productList = models.ForeignKey(Product,  on_delete=models.CASCADE,related_name='productComments')
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=1500)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.productList.name}"

    class Meta:
        db_table = 'comments'