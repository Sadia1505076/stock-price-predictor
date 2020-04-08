from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import numpy as np

from home.models import DSEHistory, DSEPrediction


@login_required()
def market_index_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        all_histories = DSEHistory.objects.raw('SELECT date, convert(date, date) as datedate, dsex_index, total_trade, total_volume, total_value, total_market_cap FROM HOME_DSEHISTORY ORDER BY date DESC')
        dse_pred = DSEPrediction.objects.raw(
            'SELECT date, convert(date, date) as datedate, future_index FROM HOME_DSEPREDICTION ORDER BY date DESC')
        # dse_pred = reversed(dse_pred)
        # all_histories = reversed(all_histories)

    context = {
        'username': username,
        'dse_pred': dse_pred,
        'dse_history': all_histories,
    }
    return render(request, 'market_index.html', context)


@login_required()
def market_stat_view(request):
    username = None
    company_names = []
    percent_change = []
    percent_change_within_100 = []

    company_names_dec = []
    percent_change_dec = []
    percent_change_within_100_dec = []

    top_price_company = []
    top_price = []
    top_price_percent = []

    top_sell_company = []
    top_sell = []
    top_sell_percent = []
    if request.user.is_authenticated:
        username = request.user.username
        inc_arr_from_file = np.load('incArr.npy')

        for x in range(0, inc_arr_from_file.shape[0]):
            company_names.append(inc_arr_from_file[x, 0])
            percent_change.append(round(float(inc_arr_from_file[x, 2]), 2))
            if float(inc_arr_from_file[x, 2]) > 100:
                percent_change_within_100.append('100')
            else:
                percent_change_within_100.append(round(float(inc_arr_from_file[x, 2]), 2))

        # --------------------------dec-----------------------------
        dec_arr_from_file = np.load('decArr.npy')
        for x in range(0, dec_arr_from_file.shape[0]):
            company_names_dec.append(dec_arr_from_file[x, 0])
            percent_change_dec.append(-round(float(dec_arr_from_file[x, 2]), 2))
            if -float(dec_arr_from_file[x, 2]) > 100:
                percent_change_within_100_dec.append('100')
            else:
                percent_change_within_100_dec.append(-round(float(dec_arr_from_file[x, 2]), 2))

        # ------------------------top price----------------------------------
        top_price_from_file = np.load('topPrice.npy', allow_pickle=True)
        for x in range(0, top_price_from_file.shape[0]):
            top_price_company.append(top_price_from_file[x, 0])
            top_price.append(top_price_from_file[x, 1])
            top_price_percent.append(round(float(top_price_from_file[x, 1])/float(top_price_from_file[0, 1])*100.0, 2))
        # -----------------------top sell------------------------------------
            top_sell_from_file = np.load('topSell.npy', allow_pickle=True)
            for x in range(0, top_sell_from_file.shape[0]):
                top_sell_company.append(top_sell_from_file[x, 0])
                top_sell.append(top_sell_from_file[x, 1])
                top_sell_percent.append(round(float(top_sell_from_file[x, 1])/float(top_sell_from_file[0, 1])*100.0, 2))

        # -------------------------doughnut 30-------------------------------
        dougnut_30 = np.load('doughnut30.npy', allow_pickle=True)
        num_inc_thirty = dougnut_30[0, 0]
        num_dec_thirty = dougnut_30[1, 0]

        dougnut_last = np.load('doughnutLast.npy', allow_pickle=True)
        num_inc_last = dougnut_last[0, 0]
        num_dec_last = dougnut_last[1, 0]

    context = {
        'username': username,
        'comp_name': company_names,
        'percent_change': percent_change,
        'within_100': percent_change_within_100,
        'comp_name_dec': company_names_dec,
        'percent_change_dec': percent_change_dec,
        'within_100_dec': percent_change_within_100_dec,
        'price_comp': top_price_company,
        'price': top_price,
        'price_percent': top_price_percent,
        'sell_comp': top_sell_company,
        'sell': top_sell,
        'sell_percent': top_sell_percent,
        'num_inc_thirty': num_inc_thirty,
        'num_dec_thirty': num_dec_thirty,
        'num_inc_last': num_inc_last,
        'num_dec_last': num_dec_last,
    }
    return render(request, 'stats.html', context)
