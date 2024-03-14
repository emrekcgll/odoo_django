from django.http import JsonResponse
from django.shortcuts import render
import xmlrpc.client


def connect_to_xmrpc():
    url = 'http://localhost:8069'
    db = 'odoo16'
    username = 'admin'
    password = 'admin'
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return models, uid, db, password


def product_list(request):
    return render(request, 'product_list.html')

def product_list_ajax(request):
    page = request.GET.get('page', 1)
    page = int(page)
    limit = 10
    offset = (page - 1) * limit

    models, uid, db, password = connect_to_xmrpc()

    total_products = models.execute_kw(db, uid, password, 'product.product', 'search_count', [[]])
    total_pages = (total_products + limit - 1) // limit
    
    product_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[]], {'offset': offset, 'limit': limit})    
    products_data_list = models.execute_kw(db, uid, password, 'product.product', 'read', [product_ids], {'fields':['category_id','brand_id', 'name', 'image']})

    return JsonResponse({'products_data_list': products_data_list, 'page':page, 'total_pages': total_pages})


def product_details(request, id):
    models, uid, db, password = connect_to_xmrpc()

    product_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[['id','=', id]]])
    product_details = models.execute_kw(db, uid, password, 'product.product', 'read', [product_ids], {'fields':['brand_id', 'name', 'image']})

    if request.method == 'POST':
        r = request.POST
        product = r.get('product')
        country = r.get('country')
        city = r.get('city')
        address = r.get('address')
        message = r.get('message')
        
        record = models.execute_kw(db, uid, password, 'request.request', 'create', [{'country': country, 'city': city, 'address': address, 'message': message, 'product_id': product_ids[0]}])

    return render(request, 'product_details.html', {'product_details': product_details[0]})