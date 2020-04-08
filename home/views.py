from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.expressions import RawSQL
from django.shortcuts import redirect, render, get_object_or_404
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from docutils.nodes import entry

from login.models import User
from .forms import EditProfileForm
from .models import Company, DSEHistory, ShareHistory, SharePrediction, DSEPrediction
from .tables import CompanyTable
import numpy as np


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # otherwise user will have to login again
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home/profile')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changePassword.html', {
        'form': form,
        'username': request.user.username,
    })


@login_required()
def home_view(request, *args, **kwargs):
    username = None
    table = None
    dates = []
    dsex_index = []
    point_color = []
    bg_color = []
    company_names = []
    percent_change = []
    percent_change_within_100 = []
    all_histories = None
    dse_pred = None

    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    # print(start_end_date[0])

    if request.user.is_authenticated:
        username = request.user.username
        # table = CompanyTable(Company.objects.all())
        # RequestConfig(request, paginate={'per_page': 15}).configure(table)

        if start_date is not None and end_date is not None:
            print("inside not none")
            print(start_date)
            all_histories = DSEHistory.objects.raw(
                'SELECT * FROM HOME_DSEHISTORY where date  between %s and %s  ORDER BY date DESC',
                [start_date, end_date])

            min_pred_query = DSEPrediction.objects.raw(
                'Select * from HOME_DSEPREDICTION where date = ( select min(date) from HOME_DSEPREDICTION  )')
            for d in min_pred_query:
                min_pred = d.date
            dse_pred = DSEPrediction.objects.raw(
                'SELECT * FROM HOME_DSEPREDICTION where date  between %s and %s ORDER BY date ASC',
                [min_pred, end_date])

        else:
            print("inside none")
            all_histories = DSEHistory.objects.raw('SELECT * FROM HOME_DSEHISTORY ORDER BY date DESC LIMIT 50')
            dse_pred = DSEPrediction.objects.raw(
                'SELECT * FROM HOME_DSEPREDICTION ORDER BY date ASC')

        for p in reversed(all_histories):
            point_color.append('red')
            bg_color.append('255, 99, 132, 0.2')
            dates.append(p.date.date())
            dsex_index.append(p.dsex_index)
        for p in dse_pred:
            dates.append(p.date.date())
            dsex_index.append(p.future_index)
            point_color.append('green')
            bg_color.append('54, 162, 235, 0.2')

        last_week_dse = DSEHistory.objects.raw(
            'Select * from HOME_DSEHISTORY where date = ( select max(date) from HOME_DSEHISTORY  )')
        for i in last_week_dse:
            last = i

        all_companies = Company.objects.all()

        pred_arr_from_file = np.load('predArr.npy')
        for x in range(0, pred_arr_from_file.shape[0]):
            company_names.append(pred_arr_from_file[x, 0])
            percent_change.append(round(float(pred_arr_from_file[x, 3]), 2))
            if float(pred_arr_from_file[x, 3]) > 100:
                percent_change_within_100.append('100')
            else:
                percent_change_within_100.append(round(float(pred_arr_from_file[x, 3]), 2))

    context = {
        'username': username,
        'table': table,
        'dates': dates,
        'indices': dsex_index,
        'last': last,
        'companies': all_companies,
        'comp_name': company_names,
        'percent_change': percent_change,
        'within_100': percent_change_within_100,
        'colors': point_color,
        'bgcolor': bg_color,

    }
    return render(request, 'Home.html', context)


@login_required()
def update_profile(request, id=None):
    instance = get_object_or_404(User, id=request.user.id)
    form = EditProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get("username"))
        instance.save()
        messages.success(request, 'Profile details updated!')
        return redirect('/home/profile')
    context = {
        'instance': instance,
        'form': form,
        'username': request.user.username,
    }
    return render(request, "editProfile.html", context)


@login_required()
def profile_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        user = User.objects.get(username=username)
        phone_number = user.phone_number

        if not first_name:
            first_name = "None"
        if not last_name:
            last_name = "None"
        if not phone_number:
            phone_number = "None"
        context = {
            'username': username,
            'first_name': first_name,
            'email': email,
            'last_name': last_name,
            'phone_number': phone_number,

        }

        return render(request, 'userProfile.html', context)


@login_required()
def company_details_view(request, *args, **kwargs):
    dates = []
    price = []
    point_color = []
    bg_color = []
    code = kwargs.get("trade_code")

    if request.method == 'GET' and code is None:
        start_date = request.GET.get('startdate')
        end_date = request.GET.get('enddate')
        print("inside get")
        print(start_date)
        search_query = request.GET.get('search_box', None)

        code = search_query.upper()

        company = Company.objects.raw('SELECT * FROM HOME_COMPANY WHERE TRADE_CODE = %s', [code])

        if start_date is not None and end_date is not None:
            company_history = ShareHistory.objects.raw(
                'SELECT id, trade_code, convert(date,date) as datedate, opening_price, max_price, min_price, closing_price, total_volume FROM HOME_SHAREHISTORY WHERE TRADE_CODE = %s and date between %s and %s ORDER BY date DESC',
                [code, start_date, end_date])

            min_pred_query = SharePrediction.objects.raw(
                'Select * from HOME_SHAREPREDICTION where date = ( select min(date) from HOME_SHAREPREDICTION  )')
            for d in min_pred_query:
                min_pred = d.date

            company_pred = SharePrediction.objects.raw(
                'SELECT id, trade_code, convert(date, date) as datedate, future_price FROM HOME_SHAREPREDICTION  WHERE TRADE_CODE = %s  and date between %s and %s ORDER BY date DESC ',
                [code, min_pred, end_date])

        else:
            company_pred = SharePrediction.objects.raw(
                'SELECT id, trade_code, convert(date, date) as datedate, future_price FROM HOME_SHAREPREDICTION  WHERE TRADE_CODE = %s ORDER BY date DESC ',
                [code])

            company_history = ShareHistory.objects.raw(
                'SELECT id, trade_code, convert(date,date) as datedate, opening_price, max_price, min_price, closing_price, total_volume FROM HOME_SHAREHISTORY WHERE TRADE_CODE = %s ORDER BY date DESC limit 30',
                [code])

        for p in reversed(company_history):
            point_color.append('red')
            bg_color.append('255, 99, 132, 0.2')
            dates.append(p.date.date())
            price.append(p.closing_price)

        for p in reversed(company_pred):
            dates.append(p.date.date())
            price.append(p.future_price)
            point_color.append('green')
            bg_color.append('54, 162, 235, 0.2')

        if company:
            for c in company:
                company = c
            context = {
                'username': request.user.username,
                'dates': dates,
                'prices': price,
                'colors': point_color,
                'bgcolor': bg_color,
                'company': company,
                'company_pred': company_pred,
                'company_history': company_history,
                'code': code,

            }
            return render(request, 'companyDetails.html', context)
        else:
            return render(request, '404_not_found.html')


def not_found(request):
    return render(request, '404_not_found.html')
