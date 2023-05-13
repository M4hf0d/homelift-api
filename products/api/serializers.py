from rest_framework import serializers
from ..models import Product , Category ,ProductRating , ProductImage , SubCategory , ProductComment , FavoriteProduct
from rest_framework.validators import UniqueValidator

 
 
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
    in_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ['rating_rv','rating_nb']
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(
                        queryset=Product.objects.all()
                    )
                ]
            }
        }
    def validate(self, data):
        if self.context['request'].method != 'PATCH':
            if data['price'] < 0:
                raise serializers.ValidationError("Price cannot be negative")
            if data['quantity'] < 0:
                raise serializers.ValidationError("Quantity cannot be negative")
            
            return data
        else: return data #No checks 
        #TODO
    
        

class FavoriteProductSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = FavoriteProduct
        # fields = '__all__'
        exclude = ['user']
     
class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)    
    class Meta:
        model = SubCategory
        # fields = ['id','name','products']
        exclude = ['categoryList']
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(
                        queryset=SubCategory.objects.all()
                    )
                ]
            }
        }

        

class CategorySerializer(serializers.ModelSerializer):
    subCategories = SubCategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(
                        queryset=Category.objects.all()
                    )
                ]
            }
        }
