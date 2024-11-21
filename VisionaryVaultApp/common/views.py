from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from VisionaryVaultApp.art.models import ArtPiece
from VisionaryVaultApp.common.models import Basket, BasketItem


class HomePageView(TemplateView):
    template_name = 'common/home.html'  # Specify the template to render

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            context['profile'] = self.request.user  # You can pass the user or profile data
        else:
            context['profile'] = None  # No profile data for unauthenticated users

        return context


def about_view(request):
    return render(request, 'common/about.html')


class BasketView(TemplateView):
    template_name = 'common/basket.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login if user is not authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the basket for the logged-in user
        basket = Basket.objects.filter(user=self.request.user).prefetch_related('items').first()

        if basket and basket.items.exists():
            total_price = sum(item.total_price for item in basket.items.all())
            basket_item_count = basket.items.count()
        else:
            total_price = 0
            basket_item_count = 0


        context['basket'] = basket
        context['total_price'] = total_price
        context['basket_item_count'] = basket_item_count
        return context


class AddToBasketView(View):
    def post(self, request, art_piece_id, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        # Retrieve the art piece object
        art_piece = get_object_or_404(ArtPiece, id=art_piece_id)

        # Get or create a basket for the user
        basket, created = Basket.objects.get_or_create(user=request.user)

        # Add the art piece to the basket or increment its quantity
        basket_item = BasketItem.objects.filter(basket=basket, art_piece=art_piece).first()

        if basket_item:
            # If the item is already in the basket, show an error message
            messages.error(request, f"This art piece is already in your basket.")
        else:
            # Otherwise, create a new basket item
            BasketItem.objects.create(basket=basket, art_piece=art_piece, quantity=1)
            messages.success(request, f"The chosen art piece has been added to your basket.")

            # Redirect to the basket view
        return redirect('view_basket')


class RemoveFromBasketView(View):
    def post(self, request, item_id):
        # Retrieve the basket item
        item = get_object_or_404(BasketItem, id=item_id)

        # Ensure the item belongs to the current user's basket
        if item.basket.user == request.user:
            item.delete()  # Remove the item from the basket

        return redirect('view_basket')


class ProcessCheckoutView(View):

    def get(self, request, *args, **kwargs):
        # Fetch basket and user profile information
        basket = Basket.objects.filter(user=request.user).first()
        profile = request.user.profile if hasattr(request.user, 'profile') else None
        total_price = sum(item.total_price for item in basket.items.all()) if basket else 0

        # Pass basket items and user's address/phone to the template
        context = {
            'basket': basket,
            'total_price': total_price,
            'profile_address': profile.address if profile else "",
            'profile_phone': profile.phone_number if profile else "",
            'profile_name': profile.full_name if profile else "",
        }
        return render(request, 'common/checkout.html', context)

    def post(self, request, *args, **kwargs):
        # Extract the form data
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')

        # Fetch the user's profile to save address and phone number
        profile = request.user.profile
        if address:
            profile.address = address
        if phone_number:
            profile.phone_number = phone_number
        profile.save()

        try:
            profile.full_clean()  # This will validate all fields of the profile
        except ValidationError as e:
            messages.error(request, f"{', '.join(e.messages)}")
            return redirect('checkout')

            # Save the profile after validation
        profile.save()

        try:
            with transaction.atomic():
                # Fetch the basket and check if it contains items
                basket = Basket.objects.filter(user=request.user).first()
                if basket and basket.items.exists():
                    # Optionally record items for the order
                    basket_items = list(basket.items.all())  # Create a list of items

                    # Process and delete each art piece before clearing the basket
                    for item in basket_items:
                        print(f"Processing {item.art_piece.description} for {name}.")
                        item.art_piece.delete()  # Delete the associated art piece

                    # Now clear the basket after processing
                    basket.items.all().delete()

                    # Add a success message
                    messages.success(request, "Your order has been processed successfully!")
                else:
                    messages.error(request, "Your basket is empty or something went wrong.")
                    return redirect('view_basket')

        except Exception as e:
            messages.error(request, f"An error occurred while processing your order: {str(e)}")
            return redirect('view_basket')

            # Redirect to an order confirmation or gallery page
        return redirect('art_gallery_list')
