from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render, get_object_or_404
from django_tables2 import RequestConfig

from login.models import User
from .forms import EditProfileForm
from .models import Company, DSEHistory, ShareHistory, SharePrediction
from .tables import CompanyTable, ShareHistoryTable, SharePredictionTable


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
def home_view(request):
    username = None
    table = None
    dates = []
    diff = []

    datesc = []
    pricec = []

    dsex_index = []
    if request.user.is_authenticated:
        username = request.user.username
        table = CompanyTable(Company.objects.all())
        RequestConfig(request, paginate={'per_page': 15}).configure(table)

        all_histories = DSEHistory.objects.raw('SELECT * FROM HOME_DSEHISTORY ORDER BY date DESC LIMIT 100')

        all_companies1 = ShareHistory.objects.raw(
            'SELECT * from HOME_SHAREHISTORY WHERE DATE(date) = \'2019-08-01\' order by date DESC')

        all_companies2 = ShareHistory.objects.raw(
            'SELECT * from HOME_SHAREHISTORY WHERE DATE(date) = \'2019-09-01\' order by date DESC')

        for p1 in all_companies1:
            for p2 in all_companies2:
                if p1.trade_code == p2.trade_code:
                    temp = []
                    temp.append(abs(p1.closing_price-p2.closing_price)/p1.closing_price*100)
                    temp.append(p1.trade_code)
                    diff.append(temp)

        # diff.sort()
        # count = 1
        for d in diff:
            print(d)
        # for i in range(11):
        #     for j in range(11):
        #         if diff[i].temp[0]> diff[j].temp[0]:

        for p in reversed(all_histories):
            # print(p.date)
            dates.append(p.date.date())
            dsex_index.append(p.dsex_index)
    all = ShareHistory.objects.raw(
            'SELECT * from HOME_SHAREHISTORY WHERE trade_code = \'ADVENT\' and DATE(date) between \'2019-08-01\' and \'2019-09-01\'')

    for p in all:
        datesc.append(p.date)
        pricec.append(p.closing_price)
    context = {
        'username': username,
        'table': table,
        'dates': dates,
        'indices': dsex_index,
        'datec': datesc,
        'price': pricec,
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
        print("inside get")
        search_query = request.GET.get('search_box', None)

        code = search_query.upper()

        company = Company.objects.raw('SELECT * FROM HOME_COMPANY WHERE TRADE_CODE = %s', [code])

        all_histories = SharePrediction.objects.raw(
            'SELECT * FROM HOME_SHAREPREDICTION  WHERE TRADE_CODE = %s ORDER BY date ASC', [code])

        # share_history = ShareHistory.objects.raw(
        #     'SELECT * FROM HOME_SHAREHISTORY ORDER BY date ASC')

        count = 1
        for p in all_histories:
            if count <= 30:
                point_color.append('red')
                bg_color.append('255, 99, 132, 0.2')
            else:
                point_color.append('green')
                bg_color.append('54, 162, 235, 0.2')
            dates.append(p.date.date())
            price.append(p.future_price)
            count = count+1

        #
        # for p in share_history:
        #     dates.append(p.date)
        #     price.append(p.closing_price)
        #     color.append('green')

        table = SharePredictionTable(all_histories)
        RequestConfig(request, paginate={'per_page': 5}).configure(table)
        if company:
            for c in company:
                cname = c.company_name
                acapital = c.authorized_capital
                pcapital = c.paid_up_capital
                snumber = c.outstanding_share_number
                sector = c.sector
            context = {
                'username': request.user.username,
                'trade_code': code,
                'company_name': cname,
                'authorized_capital': acapital,
                'paid_up_capital': pcapital,
                'outstanding_share_number': snumber,
                'sector': sector,
                'dates': dates,
                'prices': price,
                'table': table,
                'colors': point_color,
                'bgcolor': bg_color,

            }
            return render(request, 'companyDetails.html', context)
        else:
            return render(request, '404_not_found.html')
    else:
        print("inside k")

        company = Company.objects.raw('SELECT * FROM HOME_COMPANY WHERE TRADE_CODE = %s', [code])

        all_histories = ShareHistory.objects.raw(
            'SELECT * FROM HOME_SHAREPREDICTION  WHERE TRADE_CODE = %s ORDER BY date ASC', [code])

        # share_history = ShareHistory.objects.raw(
        #     'SELECT * FROM HOME_SHAREHISTORY ORDER BY date ASC')

        count = 1
        for p in all_histories:
            if count <= 30:
                point_color.append('red')
                bg_color.append('255, 99, 132, 0.2')
            else:
                point_color.append('green')
                bg_color.append('54, 162, 235, 0.2')
            dates.append(p.date.date())
            price.append(p.future_price)
            count = count + 1

        # for p in share_history:
        #     dates.append(p.date)
        #     price.append(p.closing_price)
        #     color.append('green')

        table = SharePredictionTable(all_histories)
        RequestConfig(request, paginate={'per_page': 5}).configure(table)

        for c in company:
            cname = c.company_name
            acapital = c.authorized_capital
            pcapital = c.paid_up_capital
            snumber = c.outstanding_share_number
            sector = c.sector
        context = {
            'username': request.user.username,
            'trade_code': code,
            'company_name': cname,
            'authorized_capital': acapital,
            'paid_up_capital': pcapital,
            'outstanding_share_number': snumber,
            'sector': sector,
            'dates': dates,
            'prices': price,
            'table': table,
            'colors': point_color,
            'bgcolor': bg_color,

        }
        return render(request, 'companyDetails.html', context)


def not_found(request):
    return render(request, '404_not_found.html')

