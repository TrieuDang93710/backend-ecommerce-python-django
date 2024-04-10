from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductCommentSerializer
from json import JSONDecodeError
from rest_framework.parsers import JSONParser
from backend_ecommerce.helpers import custom_response, parse_request
from .models import Category, Product, ProductImage, ProductComment
from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

# Lmf cho phần Category


class CategoryAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # đầu tiên, query tất cả record của Category
            categories = Category.objects.all()
            # sau đó, cho chúng nó vào serializer để parse từ array thành JSON
            serializer = CategorySerializer(categories, many=True)
            # nếu parse thành công thì return về cho client
            return custom_response('Get all categories successfully!', 'Success', serializer.data, 200)
        except Exception as e:
            # nếu query lỗi hay parse lỗi thì trả về error thôi
            return custom_response('Get all categories failed!', 'Error', None, 400)

    def post(self, request):
        try:
            # parse request body data từ json sang dạng mà Python hiểu được
            data = JSONParser().parse(request)
        except JSONDecodeError:
            # nếu parse error thì trả về lỗi
            return Response({
                'status': 400,
                'message': 'JSON decode error!',
                'error': None
            }, status=400)
        # nếu parse thành công thì cho data vào serializer để mapping với model
        serializer = CategorySerializer(data=data)
        # Kiểm tra xem có mapping thành công không
        if serializer.is_valid():
            # mapping thành công thì lưu record vào database và return
            serializer.save()
            return custom_response('Create category successfully!', 'Success', serializer.data, 201)
        else:
            # Nếu mapping thất bại (thiếu field required, sai kiểu dữ liệu,...) thì trả về lỗi
            return custom_response('Create category failed', 'Error', serializer.errors, 400)


class CategoryDetailAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return Category.objects.get(id=id_slug)
        except:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category)
            return custom_response('Get category successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get category failed!', 'Error', "Category not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update category successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update category failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update category failed', 'Error', "Category not found!", 400)

    def delete(self, request, id_slug):
        try:
            category = self.get_object(id_slug)
            category.delete()
            return custom_response('Delete category successfully!', 'Success', {"category_id": id_slug},
                                   204)
        except:
            return custom_response('Delete category failed!', 'Error', "Category not found!", 400)

# Phần product


class ProductViewAPI(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return custom_response('Get all products successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all products failed!', 'Error', None, 400)

    def post(self, request):
        try:
            data = parse_request(request)
        # product có ràng buộc phải có một category_id nên phải query tìm category đó trước
            category = Category.objects.get(id=data['category_id'])
            product = Product(
                name=data['name'],
                unit=data['unit'],
                price=data['price'],
                discount=data['discount'],
                amount=data['amount'],
                is_public=data['is_public'],
                thumbnail=data['thumbnail'],
                # gán category đã tìm được vào field category_id
                category_id=category
            )
            product.save()
            serializer = ProductSerializer(product)
            return custom_response('Create product successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product failed', 'Error', {"error": str(e)}, 400)


class ProductDetailAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return Product.objects.get(id=id_slug)
        except:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product failed', 'Error', "Category not found!", 400)

    def delete(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            product.delete()
            return custom_response('Delete product successfully!', 'Success', {"product_id": id_slug}, 204)
        except:
            return custom_response('Delete product failed!', 'Error', "Product not found!", 400)

# ==========================


class ProductImageAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get(self, request, product_id_slug):
        try:
            product_images = ProductImage.objects.filter(
                product_id=product_id_slug).all()
            serializers = ProductImageSerializer(product_images, many=True)
            return custom_response('Get all product images successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product images failed!', 'Error', 'Product images not found',
                                   400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            product_image = ProductImage(
                product_id=product,
                image_url=data['image_url']
            )
            product_image.save()
            serializer = ProductImageSerializer(product_image)
            return custom_response('Create product image successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product image failed', 'Error', {"error": str(e)}, 400)


class ProductImageDetailAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return ProductImage.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductImage.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_image = self.get_object(id_slug)
            serializer = ProductImageSerializer(product_image)
            return custom_response('Get product image successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product image failed!', 'Error', "Product image not found!", 400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_image = self.get_object_with_product_id(
                product_id_slug, id_slug)
            serializer = ProductImageSerializer(product_image, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product image successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product image failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product image failed', 'Error', "Product image not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_image = self.get_object_with_product_id(
                product_id_slug, id_slug)
            product_image.delete()
            return custom_response('Delete product image successfully!', 'Success', {"product_image_id":
                                                                                     id_slug}, 204)
        except:
            return custom_response('Delete product image failed!', 'Error', "Product image not found!",
                                   400)

# =====================================


class ProductCommentAPIView(views.APIView):

    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get(self, request, product_id_slug):
        try:
            product_comments = ProductComment.objects.filter(
                product_id=product_id_slug).all()
            serializers = ProductCommentSerializer(product_comments, many=True)
            return custom_response('Get all product comments successfully!', 'Success', serializers.data,
                                   200)
        except:
            return custom_response('Get all product comments failed!', 'Error', None, 400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            user = User.objects.get(id=data['user_id'])
            product_comment = ProductComment(
                product_id=product,
                rating=data['rating'],
                comment=data['comment'],
                user_id=user,
                parent_id=data['parent_id']
            )
            product_comment.save()
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Create product comment successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product comment failed', 'Error', {"error": str(e)}, 400)


class ProductCommentDetailAPIView(views.APIView):
    # Chỉ định permission_classes = [AllowAny] để cho phép tất cả các user có thể truy cập vào API này
    # Nếu không chỉ định permission_classes thì mặc định sẽ là [IsAuthenticated]
    # Còn permission_classes=[IsAdminUser] thì chỉ cho phép admin truy cập vào API này
    # Update hết tất cả các API trong project về dạng này nhé
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return ProductComment.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductComment.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_comment = self.get_object(id_slug)
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Get product comment successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product comment failed!', 'Error', "Product comment not found!",
                                   400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_comment = self.get_object_with_product_id(
                product_id_slug, id_slug)
            serializer = ProductCommentSerializer(product_comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product comment successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product comment failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product comment failed', 'Error', "Product comment notfound!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_comment = self.get_object_with_product_id(
                product_id_slug, id_slug)
            product_comment.delete()
            return custom_response('Delete product comment successfully!', 'Success', {"product_comment_id": id_slug}, 204)
        except:
            return custom_response('Delete product comment failed!', 'Error', "Product comment notfound!", 400)
