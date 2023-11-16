from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, find_avg_rating, get_images
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action) 
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def viewProduct(request,prodID):
	data = cartData(request)

	cartItems = data['cartItems']

	can_review = True

	product = Product.objects.get(id=prodID)

	reviews = product.review_set.all()

	if request.user.is_authenticated:
		customer = request.user.customer
	
		for rev in reviews:
			if rev.customer == customer:
				can_review = False
	

	avg_rating = int(find_avg_rating(reviews))

	review_images = []

	for review in reviews:
		if reviewImages.objects.filter(review=review).exists():
			imgs = reviewImages.objects.filter(review=review)
			for i in imgs:
				review_images.append(i)
	

	context = {"product":product,
	     "rating": avg_rating, 
		 "reviews":reviews,  
		 'cartItems':cartItems, 
		 'review_images':review_images,
		 'can_review':can_review
	}

	return render(request,'store/view-product.html',context)

def addReview(request):
	if request.method == 'POST':
		productname = request.POST['product']
		review = request.POST['review']
		rating = request.POST['rating']
		images = request.FILES.getlist('rev-image')
		
		verified_images = get_images(images)
		product = Product.objects.get(name = productname)
		customer = request.user.customer

		new_review, created = Review.objects.get_or_create(customer=customer, product=product, rating=rating, description = review)

		for image in verified_images:
			newImage = reviewImages.objects.create(review=new_review, image=image)
			newImage.save()

		return redirect(request.META.get('HTTP_REFERER'))
	

	
def deleteReview(request,review_id):
	rev = Review.objects.get(id=review_id)
	rev.delete()
	return redirect(request.META.get('HTTP_REFERER'))

def signup(request):
		if request.method == 'POST':
			citizenID = request.POST['citizenID']
			email = request.POST['email']
			password1 = request.POST['password1']
			password2 = request.POST['password2']

			if(password1==password2):
				if User.objects.filter(email=email).exists():
					messages.info(request,'This email already exists. Login instead?')
					return redirect(signup)
				if User.objects.filter(username=citizenID).exists():
					messages.warning(request,'Username already taken. Please try another.')
					return redirect(signup)
				else:
					newUser = User.objects.create_user(username=citizenID,email=email, password=password1)
					newUser.save()

					user_login = auth.authenticate(username=citizenID,password = password1)
					auth.login(request,user_login)

					#create a profile for the new user
					new_customer = Customer.objects.create(user=newUser, name=newUser.username, email=email)
					new_customer.save()

					messages.success(request,'Account created successfully!')
					return redirect(store)
			else:
				messages.info(request, 'Passwords do not match!')
				return redirect(signup)
		else:
			return render(request,'store/signup.html')

def login(request):
    if request.method == 'POST':
        citizenID = request.POST['citizenID']
        password = request.POST['password']
        user = auth.authenticate(username = citizenID, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(store)
        else:
            messages.info(request,'Invalid credentials')
            return redirect(login)
    return render(request, 'store/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Logged out successfully')
    return redirect(store)

@login_required
def create_seller(request):
	if request.method == 'POST':
		user = request.user
		brand = request.POST['brand']
		new_seller = Seller(user=user,brand=brand)
		new_seller.save()
		customer = Customer.objects.get(user=user)
		customer.is_seller = True
		customer.save()
		return redirect(seller_dashboard)
	else:
		return render(request,'store/sellerForm.html')

def seller_dashboard(request):
	data = cartData(request)

	cartItems = data['cartItems']

	user = request.user
	seller = Seller.objects.get(user=user)

	my_products = Product.objects.filter(seller=seller)
	no_of_products = len(my_products)

	my_reviews = []

	for product in my_products:
		if Review.objects.filter(product=product).exists():
			rev_set = Review.objects.filter(product=product)
			for rev in rev_set:
				my_reviews.append(rev)
	

	context = { 
		 'cartItems':cartItems, 
		 'seller': seller,
		 'my_products':my_products,
		 'no_of_products':no_of_products,
		 'my_reviews':my_reviews
	}

	return render(request,'store/seller-dashboard.html', context)

def addProduct(request):
	if request.method == 'POST':
		name = request.POST['name']
		price = request.POST['price']
		description = request.POST['description']
		image = request.FILES.get('image')
		digital = request.POST.get('digital',False)

		new_product = Product(name=name,price=price,description=description,image=image,digital=digital,seller=request.user.seller)
		new_product.save()

	return redirect(seller_dashboard)

def removeProduct(request,productID):
	prod = Product.objects.get(id=productID)
	prod.delete()
	return redirect(seller_dashboard)

