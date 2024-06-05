import os
from django.shortcuts import render
from django.conf import settings
import qrcode
from requests.auth import HTTPBasicAuth
import requests
from django.http import JsonResponse


def home(request):
    return render(request, 'myapp/home.html')


def fetch_external_data(request):

    if request.method == 'GET':
        item_number = request.GET.get('item_number')
        if not item_number:
            return JsonResponse({'error': 'Item number is required'}, status=400)

        # GET API call
        get_url = "https://edrx-dev1.fa.us2.oraclecloud.com/fscmRestApi/resources/11.13.18.05/itemsV2"
        get_params = {
            'q': f'ItemNumber={item_number};OrganizationCode=MFG01'
        }
        auth = HTTPBasicAuth('CSP_COMMON_USER1', 'CSP@0524May')

        try:
            response = requests.get(get_url, params=get_params, auth=auth)
            response.raise_for_status()
            get_data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        # POST API call
        post_url = "https://edrx-dev1.fa.us2.oraclecloud.com/fscmRestApi/resources/latest/availableQuantityDetails"
        post_data = {
            'ItemNumber': item_number,
            'OrganizationCode': 'MFG01'
        }

        try:
            response = requests.post(post_url, json=post_data, auth=auth)
            response.raise_for_status()
            post_data = response.json()
            # print(post_data)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        return render(request, 'myapp/information.html', {'get_response': get_data, 'post_response': post_data})

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_qr(request):
    data = 'MANGOMAZZA200ML'

    # qr_code_directory = os.path.join(settings.BASE_DIR, 'myapp', 'templates', 'images')
    qr_code_directory = os.path.join('static/img')
    if not os.path.exists(qr_code_directory):
        os.makedirs(qr_code_directory)

    QRCodefile = os.path.join(qr_code_directory, 'first.png')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    QrImage = qr.make_image(fill='black', back_color='white')
    QrImage.save(QRCodefile)

    context = {
        'qr_code_url': 'images/first.png'
    }
    return render(request, 'myapp/qr.html', context)
