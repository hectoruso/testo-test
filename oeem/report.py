# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from oeem.models import OEETiempo

from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)


class OEEMChart(ReportAdmin):
    model = OEETiempo
    fields = [
        'fecha',
        'fecha__year',
        'fecha__month',
        'fecha__day',
        'tmperdido',
        'tpperdido',
    ]
    list_group_by = ('fecha__day', 'date__month',)
    list_filter = ('maquina',)
    type = 'report'
    override_field_labels = {
        'fecha__year': lambda x, y: _('Year'),
        'fecha__month': lambda x, y: _('Month'),
        'fecha__day': lambda x, y: _('Day'),
    }


reports.register('oee-report', OEEMChart) 
#admin.register('oee-report', OEEMChart)
