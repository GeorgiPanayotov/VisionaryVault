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


class UserProfileService:
    @staticmethod
    def update_profile(user, address=None, phone_number=None):
        profile = user.profile
        if address:
            profile.address = address
        if phone_number:
            profile.phone_number = phone_number
        profile.full_clean()
        profile.save()


class BasketService:
    @staticmethod
    def process_basket(user):
        """Process the user's basket, delete art pieces, and clear the basket items."""
        try:
            with transaction.atomic():
                # Fetch the basket and check if it contains items
                basket = Basket.objects.filter(user=user).first()
                if basket and basket.items.exists():
                    # Record items for the order
                    basket_items = list(basket.items.all())  # Create a list of items

                    # Process and delete each art piece before clearing the basket
                    for item in basket_items:
                        print(f"Processing {item.art_piece.description} for {user.username}.")
                        item.art_piece.delete()  # Delete the associated art piece

                    # Now clear the basket after processing
                    basket.items.all().delete()

                    return True  # Indicate success
                else:
                    return False  # Indicates that the basket was empty or did not exist

        except Exception as e:
            # Here, we could log the error instead of sending a message to the request
            print(f"An error occurred while processing the basket: {str(e)}")
            return False

    @staticmethod
    def remove_item_from_basket(user, item_id):
        """Remove an item from the user's basket."""
        item = get_object_or_404(BasketItem, id=item_id)
        if item.basket.user == user:
            item.delete()  # Remove the item from the basket
            return True
        return False

    @staticmethod
    def add_art_piece_to_basket(user, art_piece):
        """Add an art piece to the user's basket."""
        basket, created = Basket.objects.get_or_create(user=user)

        # Check if the art piece is already in the basket
        basket_item = BasketItem.objects.filter(basket=basket, art_piece=art_piece).first()

        if basket_item:
            return False  # Art piece is already in the basket
        else:
            # If not, create a new basket item
            BasketItem.objects.create(basket=basket, art_piece=art_piece, quantity=1)
            return True

    @staticmethod
    def get_user_basket(user):
        """Retrieve the user's basket and calculate the total price and item count."""
        basket = Basket.objects.filter(user=user).prefetch_related('items').first()

        if basket and basket.items.exists():
            total_price = sum(item.total_price for item in basket.items.all())
            basket_item_count = basket.items.count()
        else:
            total_price = 0
            basket_item_count = 0

        return basket, total_price, basket_item_count


class BasketView(TemplateView):
    template_name = 'common/basket.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to log in if user is not authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the basket for the logged-in user
        basket, total_price, basket_item_count = BasketService.get_user_basket(self.request.user)

        context['basket'] = basket
        context['total_price'] = total_price
        context['basket_item_count'] = basket_item_count
        return context


class AddToBasketView(View):
    def post(self, request, art_piece_id, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        art_piece = get_object_or_404(ArtPiece, id=art_piece_id)

        # Attempt to add the art piece to the basket using the service
        if BasketService.add_art_piece_to_basket(request.user, art_piece):
            messages.success(request, "The chosen art piece has been added to your basket.")
        else:
            messages.error(request, "This art piece is already in your basket.")

            # Redirect to the basket view
        return redirect('view_basket')


class RemoveFromBasketView(View):
    def post(self, request, item_id):
        if BasketService.remove_item_from_basket(request.user, item_id):
            messages.success(request, "Item removed from your basket.")
        else:
            messages.error(request, "Could not remove the item. It may not be in your basket.")

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

        try:
            UserProfileService.update_profile(request.user, address, phone_number)
        except ValidationError as e:
            messages.error(request, f"{', '.join(e.messages)}")
            return redirect('checkout')

        if BasketService.process_basket(request.user):
            messages.success(request, "Your order has been processed successfully!")
        else:
            messages.error(request, "Your basket is empty or something went wrong.")

        return redirect('art_gallery_list')
