from rest_framework import status,generics,mixins,viewsets
  #filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView ,RetrieveUpdateDestroyAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound , ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND
import django_filters.rest_framework as filters
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from users.models import Customer
from rest_framework import permissions 




from ..models import Product , Category , SubCategory , ProductImage , ProductRating , ProductComment ,FavoriteProduct
from .serializers import ProductSerializer ,CategorySerializer , SubCategorySerializer , ImagesSerializer , RatingSerializer , CommentsSerializer , FavoriteProductSerializer
from .filter import ProductFilter



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name','description','category__name', 'subcategory__name']
    ordering_fields = ['name', 'price','quantity']
    
class FavoriteProductViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteProductSerializer

    def get_queryset(self):
        # print("###########",self.request.user)
        customer = self.request.user
        return FavoriteProduct.objects.filter(user=customer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the product already exists in the favorite products list
        customer = self.request.user
        product = serializer.validated_data['product']
        favorite_product = FavoriteProduct.objects.filter(user=customer, product=product)
        # print("$$$$$$$$$$",favorite_product)
        if favorite_product.first():
            return Response({"message": "Product is already in favorite list"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user of the new FavoriteProduct to the current authenticated user
        serializer.validated_data['user'] = customer

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Favorite product deleted successfully.'},status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImagesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImagesSerializer
    
class ImagesCreateAPIView(generics.CreateAPIView):
    serializer_class = ImagesSerializer
    queryset = ProductImage.objects.all()
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
      
        productlist = Product.objects.get(pk=pk)
        image = ProductImage.objects.filter(productList=productlist)
        # image = ProductImage.objects.filter(productList=productlist,imge=self.request.data['image'])
        if image.count() >= 5:
            raise ValidationError('u have already 5 images')
        productlist.save()
        serializer.save(productList=productlist)
    


class ImagesListAPIView(generics.ListAPIView):
    serializer_class = ImagesSerializer

    def get_queryset(self):
        pk =self.kwargs['pk']
        return ProductImage.objects.filter(productList=pk)




    



class CommentsListAPIView(generics.ListAPIView):
    serializer_class = CommentsSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return ProductComment.objects.filter(productList=pk)
    
class CommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    queryset = ProductComment.objects.all()
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        print('$$$$$$$$$')
        print(pk)
        productlist = Product.objects.get(pk=pk)
        comment_user = self.request.user
        comment = ProductComment.objects.filter(productList=productlist,comment_user=comment_user)
        if comment.exists():
            raise  ValidationError('you have already a comment')
        productlist.save()
        serializer.save(productList=productlist,comment_user=comment_user  )
        
class CommentsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = CommentsSerializer


class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    queryset = ProductRating
    def perform_create(self, serializer):   
        pk = self.kwargs['pk']
        productlist = Product.objects.get(pk=pk)
        rating_user = self.request.user
        rating = ProductRating.objects.filter(productList=productlist,rating_user=rating_user)
        if rating.exists():
            raise ValidationError('u have already rating ')
        if productlist.rating_nb == 0:
            # serializer.validated_data['rating'] or self.request.data['rating'] but with int
            productlist.rating_rv = serializer.validated_data['rating']
        else :
            productlist.rating_rv = (productlist.rating_rv + serializer.validated_data['rating'])/2
        productlist.rating_nb = productlist.rating_nb +1
            
        
        productlist.save()
        serializer.save(productList=productlist,rating_user=rating_user)


class RatingListAPIView(generics.ListAPIView):
    serializer_class = RatingSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return ProductRating.objects.filter(productList=pk)


class RatingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    queryset = ProductRating   


class SubCategoryListAPIView(ListAPIView):
    serializer_class = SubCategorySerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SubCategory.objects.filter(categoryList=pk)


class SubCategoryCreateAPIView(CreateAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        categorylist = Category.objects.get(pk=pk)
        subcategory = SubCategory.objects.filter(categoryList=categorylist,name=self.request.data['name'])

        if subcategory.exists():
            raise ValidationError('you have already this subcategory')
        categorylist.save()
        serializer.save(categoryList=categorylist)
        


class SubCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    
