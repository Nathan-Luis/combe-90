from django.contrib import admin
from django.utils.html import format_html
from .models import Quotation, StockQuantity, MailingList, Contact, Product, QuotationItem, Service, SurveyRequest, CarouselImage, SurveyImage

# Register MailingList model
@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    actions = ['delete_selected']


# Inline to display Quotation Items in the Quotation admin view
class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0  # No extra empty rows
    readonly_fields = ['total_price', 'product', 'quantity', 'unit_price']  # Ensure fields are read-only
    fields = ['product', 'quantity', 'unit_price', 'total_price']  # Fields to display

    def total_price(self, obj):
        # Dynamically calculate total price
        return obj.unit_price * obj.quantity


# Register Quotation model with QuotationItem inline
@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'date_created', 'name', 'email', 'phone', 'total_amount', 'settled', 'delivered', 'deleted')
    search_fields = ('reference', 'name', 'email')
    list_filter = ('settled', 'delivered', 'deleted')
    inlines = [QuotationItemInline]  # Display Quotation items inline
    fields = ['reference', 'date_created', 'name', 'email', 'phone', 'total_amount', 'settled', 'delivered', 'deleted']


# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity')
    search_fields = ('name',)
    list_filter = ('price', 'stock_quantity')
    fields = ('name', 'description', 'price', 'stock_quantity', 'image')
    actions = ['delete_selected']


# Register StockQuantity without custom admin classes
#admin.site.register(StockQuantity)


# Register Contact model with custom admin class
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone', 'date_submitted', 'contacted')
    list_filter = ('contacted', 'date_submitted')
    search_fields = ('first_name', 'email', 'phone')
    actions = ['mark_as_contacted']

    def mark_as_contacted(self, request, queryset):
        queryset.update(contacted=True)
    mark_as_contacted.short_description = "Mark selected contacts as contacted"

admin.site.register(Contact, ContactAdmin)


# Register Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'image')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'image')

    def description_short(self, obj):
        # Shorten the description for display with "..." if too long
        return obj.description[:75] + '...' if len(obj.description) > 75 else obj.description
    description_short.short_description = 'Description'


# Inline for displaying Survey Images in SurveyRequest
class SurveyImageInline(admin.TabularInline):
    model = SurveyImage
    extra = 1  # Number of extra empty rows for adding images
    readonly_fields = ['image']  # Display the image


# Custom method to display image previews in the SurveyRequest admin
class SurveyRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'survey_address', 'requested_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('requested_at',)
    inlines = [SurveyImageInline]  # Display the SurveyImage inline

    # Adding a method to display image previews with improved scrolling
    def image_preview(self, obj):
        images = SurveyImage.objects.filter(survey_request=obj)
        image_html = ""
        for img in images:
            image_html += f'<div style="display: inline-block; margin-right: 10px;"><img src="{img.image.url}" style="max-height: 150px;" /></div>'
        return format_html(
            '<div style="white-space: nowrap; overflow-x: scroll; max-width: 100%; display: flex; scrollbar-width: thin;">{}</div>'
            '<style>'
            'div[style*="overflow-x: scroll"] {{'
            'scroll-behavior: smooth;'
            '-webkit-overflow-scrolling: touch;'
            '}}'
            'div[style*="overflow-x: scroll"]::-webkit-scrollbar {{'
            'height: 6px;'
            '}}'
            'div[style*="overflow-x: scroll"]::-webkit-scrollbar-thumb {{'
            'background-color: darkgrey;'
            'border-radius: 3px;'
            '}}'
            '</style>',
            format_html(image_html)
        )

    image_preview.short_description = "Image Preview"
    readonly_fields = ['image_preview']

    # Customize admin template to add the image preview section
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'survey_address', 'survey_type', 'geo_location', 'additional_info', 'image_preview')
        }),
    )


# Register SurveyRequest model with SurveyImage inline and image preview
admin.site.register(SurveyRequest, SurveyRequestAdmin)


# Register CarouselImage model
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image')
