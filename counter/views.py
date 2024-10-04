
from django.http import HttpResponse
# from django.contrib import redirects
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages


from table.models import SubmittedItem

import logging

from django.shortcuts import get_object_or_404, redirect
from table.models import orders
logger = logging.getLogger(__name__)
from table.models import SubmittedItem
def counter_home(request):
    # table_numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # context={'table_numbers':table_numbers}

    # order= SubmittedItem.objects.all()
    # # print(order)
    # context = {'orders': order}
    # return render(request,'counter/counter_home.html',context)


    # return render(request, 'counter/counter_home.html', {
    #     'tables_with_orders': tables_with_orders
    # })




    confirmed_orders = SubmittedItem.objects.filter(status='confirmed').order_by('tableNumber')

    # Organize confirmed orders by tableNumber
    tables_with_confirmed_orders = {}
    
    for order in confirmed_orders:
        table_number = order.tableNumber
        if table_number not in tables_with_confirmed_orders:
            tables_with_confirmed_orders[table_number] = []
        tables_with_confirmed_orders[table_number].append(order)

    # Pass the combined dictionary to the template
    return render(request, 'counter/counter_home.html', {
        'tables_with_confirmed_orders': tables_with_confirmed_orders
    })



def confirm_order(request, table_number):
    if request.method == 'POST':
        # Fetch all pending orders for the specified table
        pending_orders = SubmittedItem.objects.filter(tableNumber=table_number, status='pending')

        # Update the status of each order to 'confirmed'
        pending_orders.update(status='confirmed')
        
        # Redirect back to the kitchen home after confirmation
        return redirect('counter_home')

def confirm_all_orders(request, table_number):
    if request.method == 'POST':
        # Get all pending orders for the specified table
        all_orders = orders.objects.filter(tableNumber=table_number, status='pending')
        
        # Update status for all pending orders
        for order in all_orders:
            order.status = 'confirmed'
            order.save()
        
        # Redirect or render a success message
        return redirect('counter_home')  # Redirect to the kitchen home page



def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('counter_home')
        else:
            messages.error(request,'Invalid user or password..')
            return render(request,'counter/login.html')
    return render(request,"counter/login.html")

def logout_view(request):
    logout(request)
    return login_view(request)







def menu(request):
    return render(request,'counter/menu.html')

def tableList1(request):
    tab=request.GET.get('tab','recent')
    table_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]  # Example: Replace with your logic to get table numbers
    if tab == 'all':
        template_name = 'counter/tableList.html'
        context = {'table_numbers': table_numbers}
    else:
        template_name = 'counter/counter_home.html'
        context = {'table_numbers': table_numbers}

    return render(request, template_name, context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_table_receipt(request, table_number):
    # print(f"Table number requested: {table_number}")
    receipt_data = {
        "1": {
            "customer_name": "John Doe",
            "order_no": "1",
            "date": "15th September 2024",
            "items": [
                {"item": "Grilled Chicken", "qty": 2, "price": "$10.00", "total": "$20.00"},
                {"item": "French Fries", "qty": 1, "price": "$05.00", "total": "$05.00"},
                {"item": "Soda", "qty": 2, "price": "$03.00", "total": "$06.00"},
            ],
            "subtotal": "$31.00",
            "tax": "$2.48",
            "total": "$33.48"
        },
        "2": {
            "customer_name": "Jane Smith",
            "order_no": "789012",
            "date": "16th September 2024",
            "items": [
                {"item": "Burger", "qty": 1, "price": "$8.00", "total": "$8.00"},
                {"item": "Salad", "qty": 1, "price": "$6.00", "total": "$6.00"},
                {"item": "Juice", "qty": 1, "price": "$4.00", "total": "$4.00"},
            ],
            "subtotal": "$18.00",
            "tax": "$1.44",
            "total": "$19.44"
        }
        # Add more table numbers as needed
    }

    # Fetch data based on table_number or return an error if not found
    data = receipt_data.get(str(table_number), {
        "error": "No data found for this table number."
    })

    return JsonResponse(data)
