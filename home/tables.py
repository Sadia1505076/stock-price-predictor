import django_tables2 as tables
from .models import Company, ShareHistory, SharePrediction
from django_tables2.utils import A


class CompanyTable(tables.Table):
    trade_code = tables.LinkColumn("home:company_detail", args=[A('pk')])

    class Meta:
        model = Company
        template_name = 'django_tables2/bootstrap-responsive.html'


class ShareHistoryTable(tables.Table):
    # trade_code = tables.LinkColumn("home:company_detail", args=[A('pk')])
    class Meta:
        model = ShareHistory
        template_name = 'django_tables2/bootstrap-responsive.html'


class SharePredictionTable(tables.Table):
    # trade_code = tables.LinkColumn("home:company_detail", args=[A('pk')])
    class Meta:
        model = SharePrediction
        template_name = 'django_tables2/bootstrap-responsive.html'
