from django.shortcuts import render,get_object_or_404

# Create your views here.
from table.models import Category,FoodItem
from table.models import SubmittedItem

def table_home(request, id=None):
    categories = Category.objects.all()
    table_number = request.session.get('table_number', None) 

    if id:  # if a category ID is provided in the URL
        selected_category = get_object_or_404(Category, id=id)
    else:  # otherwise, show the first category by default
        selected_category = categories.first()

    # Get the food items for the selected category
    food_items = FoodItem.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'food_items': food_items,
        'table_number': table_number
    }


    if request.method == 'POST':
        # Get the table number from the submitted form data
        table_number = request.POST.get('tableNumber')
        
        # Store the table number in the user's session
        request.session['tableNumber'] = table_number  # This allows you to access it later

        # Save the submitted item in the database
        SubmittedItem.objects.create(tableNumber=table_number, )  # Save other necessary fields
        print(f"Current Table Number: {table_number}")
    return render(request, 'table_home.html', context)
