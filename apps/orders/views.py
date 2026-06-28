from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import json

from .models import Order, OrderItem
from apps.products.models import Product


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    orders = (
        Order.objects.select_related('user')
        .prefetch_related('items__product')
        .all()
    )

    if not request.user.is_staff:
        orders = orders.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='login')
def checkout_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        cart_data_raw = request.POST.get('cart_data', '[]')
        
        try:
            cart_items = json.loads(cart_data_raw)
        except json.JSONDecodeError:
            messages.error(request, "Savat ma'lumotlari xato shaklda.")
            return redirect('product_list')
            
        if not cart_items:
            messages.error(request, "Savatingiz bo'sh. Savatga mahsulot qo'shing.")
            return redirect('product_list')
            
        if not address:
            messages.error(request, "Iltimos, yetkazib berish manzilini kiriting.")
            return render(request, 'orders/checkout.html', {
                'full_name': full_name,
                'phone': phone,
                'address': address,
                'cart_data': cart_data_raw
            })
            
        try:
            with transaction.atomic():
                # 1. Create order
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name or f"{request.user.first_name} {request.user.last_name}".strip(),
                    phone=phone or request.user.phone_number,
                    address=address,
                )
                
                # 2. Process items
                for item in cart_items:
                    product_id = item.get('id')
                    qty = int(item.get('qty', 1))
                    
                    product = Product.objects.select_for_update().get(id=product_id)
                    
                    if not product.is_active or product.stock < qty:
                        raise ValueError(f"Kechirasiz, '{product.name}' mahsulotidan omborda yetarli emas yoki sotuvda yo'q.")
                        
                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        unit_price=product.price,
                        quantity=qty
                    )
                    
                    # Update stock
                    product.stock -= qty
                    product.save(update_fields=('stock',))
                    
                # 3. Update order total
                order.update_total()
                
            messages.success(request, "Buyurtmangiz muvaffaqiyatli rasmiylashtirildi!")
            return redirect('/orders/?checkout_success=1')
            
        except Product.DoesNotExist:
            messages.error(request, "Tanlangan mahsulot tizimda topilmadi.")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
            
    return render(request, 'orders/checkout.html')
