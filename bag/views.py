from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # Handle case with product size
        if item_id in bag:
            # Ensure bag[item_id] is a dictionary
            if isinstance(bag[item_id], int):
                # Convert to dictionary format if currently an integer
                bag[item_id] = {'items_by_size': {}, 'quantity': bag[item_id]}

            # Now handle the items by size
            if size in bag[item_id].get('items_by_size', {}):
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id].setdefault('items_by_size', {})[size] = quantity
        else:
            # Initialize with size
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # Handle case without product size
        if item_id in bag:
            # Ensure bag[item_id] is treated correctly
            if isinstance(bag[item_id], dict):
                # If it's already a dictionary, add to the quantity
                bag[item_id]['quantity'] = bag[item_id].get('quantity', 0) + quantity
            else:
                # If it's an integer, just add the quantity
                bag[item_id] += quantity
        else:
            # Initialize without size
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)