from rest_framework import serializers
from ..models import Product , Category ,ProductRating , ProductImage , SubCategory , ProductComment
 
 
 
class ImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        exclude = ['productList']
        # fields = "__all__"
        
class RatingSerializer(serializers.ModelSerializer):
    rating_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ProductRating
        # fields = "__all__"
        exclude = ['productList']

        
 
class CommentsSerializer(serializers.ModelSerializer):
    comment_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ProductComment
        exclude = ['productList']
 

class ProductSerializer(serializers.ModelSerializer):
    productComments = CommentsSerializer(many=True,read_only=True)
    productImages = ImagesSerializer(many=True,read_only=True)
    productRatings = RatingSerializer(many=True,read_only=True)
    category_name = serializers.CharField(source='category.name',read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name',read_only=True)
    

    
    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ['rating_rv','rating_nb']
        
        
class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    
    class Meta:
        model = SubCategory
        # fields = ['id','name','products']
        exclude = ['categoryList']
        

class CategorySerializer(serializers.ModelSerializer):
    subCategories = SubCategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = "__all__"
