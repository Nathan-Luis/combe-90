import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Quotation, QuotationItem, StockQuantity, MailingList, Product, Service, SurveyRequest, CarouselImage, SurveyImage
from django.utils import timezone
from django.db import IntegrityError
from .forms import ContactForm, ProductStockForm, MailingListForm, SurveyRequestForm

def index(request):
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Thank you for subscribing!')
                return redirect('index')
            except IntegrityError:
                messages.error(request, 'This email is already subscribed.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MailingListForm()

    return render(request, 'index.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def about_us(request):
    carousel_images = CarouselImage.objects.all()
    return render(request, 'about-us.html', {'carousel_images': carousel_images})

def cart(request):
    return render(request, 'cart.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for getting in touch! We will contact you soon.')
            return redirect('contact_us')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ContactForm()

    return render(request, 'contact-us.html', {'form': form})

def products(request):
    return render(request, 'products.html')

def quotation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reference = data.get('reference')
            total_amount = data.get('total_amount', 0)
            items = data.get('items')

            if not reference or not total_amount or not items:
                raise ValueError("Missing required fields")

            quotation = Quotation.objects.create(
                reference=reference,
                date_created=timezone.now(),
                total_amount=total_amount,
                settled=False,
                delivered=False,
                deleted=False
            )

            for item in items:
                product_name = item.get('product_name')
                quantity = int(item.get('quantity', 0))
                unit_price = float(item.get('unit_price', 0))
                total_price = quantity * unit_price

                try:
                    product = Product.objects.get(name=product_name)
                except Product.DoesNotExist:
                    messages.error(request, f'Product "{product_name}" does not exist.')
                    return render(request, 'quotation.html')

                QuotationItem.objects.create(
                    quotation=quotation,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )

            messages.success(request, 'Quotation created successfully!')
            return redirect('quotation')

        except (KeyError, ValueError) as e:
            messages.error(request, f'Error processing quotation: {e}')
            return render(request, 'quotation.html')

    return render(request, 'quotation.html')

def subscribe_email(request):
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Thank you for subscribing!')
                return redirect('success_page')
            except IntegrityError:
                messages.error(request, 'This email is already subscribed.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MailingListForm()

    return render(request, 'index.html', {'form': form})

def admin_view(request):
    return render(request, 'admin.html')

def admin_mailing_list(request):
    mailing_list = MailingList.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                MailingList.objects.create(email=email)
                messages.success(request, 'Email added successfully!')
            except IntegrityError:
                messages.error(request, 'This email is already subscribed.')
    return render(request, 'admin_mailing_list.html', {'mailing_list': mailing_list})

def admin_quotations(request):
    quotations = Quotation.objects.all()
    return render(request, 'admin_quotations.html', {'quotations': quotations})

def delete_mailing_list(request, pk):
    email = get_object_or_404(MailingList, pk=pk)
    email.delete()
    messages.success(request, 'Email deleted successfully!')
    return redirect('admin_mailing_list')

def view_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    items = QuotationItem.objects.filter(quotation=quotation)
    return render(request, 'admin_quotation_details.html', {'quotation': quotation, 'items': items})

def delete_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation.delete()
    messages.success(request, 'Quotation deleted successfully!')
    return redirect('admin_quotations')

def update_stock_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductStockForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductStockForm(instance=product)

    return render(request, 'update_stock.html', {'form': form, 'product': product})

def services(request):
    services = Service.objects.all()
    form = SurveyRequestForm()

    return render(request, 'services.html', {
        'services': services,
        'form': form
    })

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    form = SurveyRequestForm()

    if request.method == 'POST':
        form = SurveyRequestForm(request.POST, request.FILES)
        if form.is_valid():
            survey_request = form.save()

            # Handle multiple images (maximum 10)
            images = request.FILES.getlist('images')
            for image in images[:10]:
                SurveyImage.objects.create(survey_request=survey_request, image=image)

            messages.success(request, 'Survey request submitted successfully!')
            return redirect('service_detail', service_id=service_id)

    return render(request, 'service_detail.html', {'service': service, 'form': form})

def submit_survey_request(request):
    if request.method == 'POST':
        form = SurveyRequestForm(request.POST, request.FILES)
        if form.is_valid():
            survey_request = form.save()

            # Handle multiple images (maximum 10)
            images = request.FILES.getlist('images')
            for image in images[:10]:
                SurveyImage.objects.create(survey_request=survey_request, image=image)

            messages.success(request, 'Survey request submitted successfully!')
            return redirect('services')
        else:
            return render(request, 'services.html', {'form': form, 'error': 'Form data is invalid.'})
    return HttpResponse('Method not allowed', status=405)

def get_service_details(request, id):
    service = get_object_or_404(Service, id=id)
    # Ensure that the view responds with JSON
    return JsonResponse({
        'name': service.name,
        'description': service.description,
        'image_url': service.image.url if service.image else ''
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def index(request):
    services = Service.objects.all()  # Fetch all services
    return render(request, 'index.html', {'services': services})