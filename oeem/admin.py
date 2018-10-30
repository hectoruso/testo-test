#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Instalacion, Plantel, MantPreventivoOT, Maquina, SalidaOT, CerrarOt, Personal, PersonalP, Material, \
    MaterialMaquina, RegistroMaquinas, MantPreventivo, Existencias, Ingresos, Salida, \
    MaterialMantenimiento, Ot, Instalaciones
from django.forms import ModelForm
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget, NumberInput, EnclosedInput, \
    LinkedSelect, Select, AutosizedTextarea
from import_export.admin import ImportExportActionModelAdmin
import adminactions.actions as actions
import datetime
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from easy_pdf.rendering import render_to_pdf_response


class PrevManto(ModelForm):
    class Meta:
        model = MantPreventivo
        fields = '__all__'
        widgets = {
            'maquina': LinkedSelect,
            'ndate': SuitDateWidget,
            'ldate': SuitDateWidget,
            'nhours': NumberInput(attrs={'class': 'input-mini'}),
            'lhours': NumberInput(attrs={'class': 'input-mini'}),
            'lapso': NumberInput(attrs={'class': 'input-mini'}),
            'intervalo': Select(attrs={'class': 'input-small'}),
            'status': Select(attrs={'class': 'input-small'}),
        }


class CierreOtForm(ModelForm):
    class Meta:
        model = CerrarOt
        fields = '__all__'
        widgets = {
            'fin': SuitSplitDateTimeWidget,
            'inicio': SuitSplitDateTimeWidget,
            'cierre': SuitDateWidget,
            'tiempo': NumberInput(attrs={'class': 'input-mini'}),
        }

class RegistroForm(ModelForm):
    class Meta:
        model = RegistroMaquinas
        fields = '__all__'
        widgets = {
            'maquina': LinkedSelect,
	    'ubicacion': LinkedSelect,
        }

class InventarioForm(ModelForm):
    class Meta:
        model = Existencias
        fields = '__all__'
        widgets = {
            'material': LinkedSelect,
        }

class SalidaOTInlineForm(ModelForm):
    class Meta:
        model = SalidaOT
        fields = '__all__'
        widgets = {
            'fecha': SuitDateWidget,
            'material': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
            'receptor': Select(attrs={'class': 'input-medium'}),
        }


class OTForm(ModelForm):
    class Meta:
        model = Ot
        fields = '__all__'
        widgets = {
            'maquina': LinkedSelect,
            'fecha': SuitSplitDateTimeWidget,
            'solicita': LinkedSelect,
            'asignado': LinkedSelect,
            'departamento': Select(attrs={'class': 'input-small'}),
            # 'descripcion': AutosizedTextarea(attrs={'rows': 4, 'class': 'input-xlarge'}),

        }


class EjecPrevForm(ModelForm):
    class Meta:
        model = MantPreventivoOT
        fields = '__all__'
        widgets = {
            'maquina': LinkedSelect,
            'prev': LinkedSelect,
            'fecha': SuitDateWidget,
            'horas': NumberInput(attrs={'class': 'input-mini'}),
            'tiempo': NumberInput(attrs={'class': 'input-mini'}),
        }


class MMInlineForm(ModelForm):
    class Meta:
        model = MaterialMantenimiento
        fields = '__all__'
        widgets = {
            'materiales': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
        }


class MMForm(ModelForm):
    class Meta:
        model = MaterialMantenimiento
        fields = '__all__'
        widgets = {
            'manto': LinkedSelect,
            'materiales': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
        }


class IngresoInlineForm(ModelForm):
    class Meta:
        model = Salida
        fields = '__all__'
        widgets = {
            'fecha': SuitDateWidget,
            'material': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
            'receptor': Select(attrs={'class': 'input-medium'}),
        }


class SalidaInlineForm(ModelForm):
    class Meta:
        model = Salida
        fields = '__all__'
        widgets = {
            'fecha': SuitDateWidget,
            'material': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
            'receptor': Select(attrs={'class': 'input-medium'}),
        }


class SalidaForm(ModelForm):
    class Meta:
        model = Salida
        fields = '__all__'
        widgets = {
            'fecha': SuitDateWidget,
            'material': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
            'unidad': Select(attrs={'class': 'input-small'}),
            'receptor': Select(attrs={'class': 'input-medium'}),
            'maquina': LinkedSelect,
            'horas': NumberInput(attrs={'class': 'input-small'}),
        }


class MaterialInlineForm(ModelForm):
    class Meta:
        model = MaterialMaquina
        fields = '__all__'
        widgets = {
            'material': LinkedSelect,
            'cantidad': NumberInput(attrs={'class': 'input-mini'}),
        }


class CierreOtInline(admin.StackedInline):
    model = CerrarOt
    form = CierreOtForm
    fields = (('horas', 'tiempo'),('inicio'), ('fin'), (('ejecucion', 'observaciones')), 'cierre')

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class MaterialAdminInline(admin.TabularInline):
    model = MaterialMaquina
    form = MaterialInlineForm
    raw_id_fields = ('material',)

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class SalidaInline(admin.TabularInline):
    model = Salida
    form = SalidaInlineForm
    fields = ('fecha', 'material', 'cantidad', 'unidad', 'receptor')
    raw_id_fields = ('material',)

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class SalidaOTInline(admin.TabularInline):
    model = SalidaOT
    form = SalidaOTInlineForm
    fields = ('fecha', 'material', 'cantidad', 'unidad', 'receptor')
    raw_id_fields = ('material',)

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class MaterialMantenimientoInline(admin.TabularInline):
    model = MaterialMantenimiento
    form = MMInlineForm
    fields = ('cantidad', 'materiales', 'unidad')
    raw_id_fields = ('materiales',)

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class MaquinaAdmin(admin.ModelAdmin):
    fields = ('descripcion', 'marca', 'modelo')
    list_display = ('descripcion', 'marca', 'modelo')
    inlines = [MaterialAdminInline, ]
    list_filter = ('descripcion', 'marca')


class MaterialAdmin(admin.ModelAdmin):
    fields = ('descripcion', 'partnumber')
    list_display = ('descripcion', 'partnumber')
    search_fields = ['descripcion', 'partnumber']


class RegistroMaquinasAdmin(admin.ModelAdmin):
    form = RegistroForm
    raw_id_fields = ('maquina', 'ubicacion',)
    fields = ('codigo', 'maquina', 'serie', 'horas', 'area', 'ubicacion')
    list_display = ('codigo', 'maquina', 'serie', 'horas', 'ubicacion')
    list_editable = ('horas',)
    inlines = [SalidaInline, ]
    list_filter = ('area', 'ubicacion')
    actions_on_top = True
    lists_per_page = 50

class ExistenciasAdmin(admin.ModelAdmin):
    form = InventarioForm
    raw_id_fields = ('material',)
    fields = ('material', 'cantidad', 'unidad')
    list_display = ('material', 'cantidad', 'unidad')
    list_filter = ('material__descripcion',)
    search_fields = ['material__descripcion', 'material__partnumber']


class IngresosAdmin(admin.ModelAdmin):
    form = IngresoInlineForm
    fields = ('fecha', 'material', 'cantidad', 'unidad', 'receptor')
    list_display = ('fecha', 'material', 'cantidad', 'unidad', 'receptor')
    list_filter = ('material__descripcion', 'fecha')
    raw_id_fields = ('material',)


class SalidaAdmin(admin.ModelAdmin):
    form = SalidaForm
    raw_id_fields = ('material', 'maquina',)
    fields = ('fecha', 'material', ('cantidad', 'unidad'), ('maquina', 'horas'), 'receptor')
    list_display = ('fecha', 'material', 'cantidad', 'unidad', 'maquina', 'horas', 'receptor')
    list_filter = ('material__descripcion', 'fecha')
    search_fields = ['material__descripcion', 'fecha']


class PrevManto(admin.ModelAdmin):
    form = PrevManto
    raw_id_fields = ('maquina',)
    fields = (
        'maquina', ('tarea'), ('intervalo'), ('ldate'), ('ndate'), ('lapso'), ('nhours', 'lhours'), ('descripcion'),
        'status')
    list_display = ('maquina', 'tarea', 'status', 'ndate', 'nhours')
    list_filter = ('maquina', 'status')
    actions = ['update_status', 'Generar_OT']

    def update_status(self, request, queryset):
        queryset.filter(nhours__lte=100).filter(nhours__gte=0).update(status='p')
        queryset.filter(nhours__lt=0).update(status='r')
        queryset.filter(ndate__lte=datetime.date.today()).update(status='r')

    update_status.short_description = 'Actualizar Estado'

    def Generar_OT(self, request, queryset):
        for mantpreventivo in queryset:
            maquina = mantpreventivo.maquina
            tarea = (('%s.\n %s') % (mantpreventivo.tarea, mantpreventivo.descripcion))
            user = User.objects.get(id=1)
            Ot.objects.create(descripcion=tarea, fecha=datetime.datetime.now(), criticidad='m', maquina=maquina,
                              solicita=user, departamento='m', tipo='p', mantoid=mantpreventivo.id)

    def suit_cell_attributes(self, obj, column):
        if obj.status == 'r':
            return {'class': 'text-error'}
        elif obj.status == 'c':
            return {'class': 'text-success'}
        else:
            return {'class': 'text-warning'}


class OTAdmin(admin.ModelAdmin):
    form = OTForm
    model = Ot
    inlines = [CierreOtInline, SalidaOTInline, ]
    radio_fields = {'relacionado': admin.HORIZONTAL, 'criticidad': admin.HORIZONTAL, 'tipo': admin.HORIZONTAL}
    fieldsets = [
        ('Orden de Trabajo',
         {'classes': ('suit-tab suit-tab-ot'), 'fields': [('departamento'), ('relacionado'),
                                                          ('criticidad'), ('tipo'), ('maquina', 'asignado'),
                                                          'descripcion']}),
    ]
    raw_id_fields = ('maquina', 'solicita', 'asignado',)
    list_display = ('fecha', 'maquina', 'asignado', 'prog', 'status', 'cierre')
    actions = ['report_pdf']

    def suit_cell_attributes(self, obj, column):
        if obj.status == 'p':
            return {'class': 'text-error'}
        elif obj.status == 'c':
            return {'class': 'text-success'}
        else:
            return {'class': 'text-warning'}

    def report_pdf(self, request, queryset):
        template = ('report.html')
        dpt = {'m': 'Mantenimiento', 'l': 'Logistica', 'p': 'Produccion', 'c': 'Calidad', 'v': 'Ventas', 'o': 'Otros'}
        rl = {'c': 'Calidad', 'i': 'Inocuidad', 'o': 'Operacion', 'e': 'Eficiencia', 's': 'Seguridad'}
        tp = {'c': 'Correctivo', 'p': 'Preventivo', 'l': 'Limpieza'}
        cr = {'a': 'Alta', 'm': 'Media', 'b': 'Moderada'}
        for ot in queryset:
            otn = ot.idn
            fecha = ot.fecha
            res = ot.asignado
            depart = dpt[ot.departamento]
            us = User.objects.get(username=ot.solicita)
            usuario = str(us.first_name + ' ' + us.last_name)
            tipo = tp[ot.tipo]
            criti = cr[ot.criticidad]
            inci = rl[ot.relacionado]
            descri = ot.descripcion
            context = {
                'id': otn, 'fecha': fecha, 'departamento': depart, 'usuario': usuario, 'tipo': tipo,
                'criticidad': criti, 'incidencia': inci, 'maquina': ot.maquina, 'responsable': res,
                'descripcion': descri
            }
            return render_to_pdf_response(request, template, context)

    report_pdf.short_description = 'Exportar Orden de Trabajo'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            print (str(request.user))
            obj.solicita = request.user
        super(OTAdmin, self).save_model(request, obj, form, change)


class MMantoAdmin(admin.ModelAdmin):
    form = MMForm
    model = MaterialMantenimiento
    raw_id_fields = ('manto', 'materiales',)
    fields = ('manto', 'materiales', 'cantidad', 'unidad')
    list_display = ('manto', 'materiales', 'cantidad', 'unidad')


class MMQAdmin(admin.ModelAdmin):
    model = MaterialMaquina
    list_display = ('material', 'maquina', 'cantidad', 'unidad')
    list_filter = ('maquina',)


class MantPrevOTAdmin(admin.ModelAdmin):
    form = EjecPrevForm
    model = MantPreventivoOT
    raw_id_fields = ('maquina', 'prev',)
    fieldsets = (
        ('Datos Generales', {'fields': (('prev', 'tiempo'), ('fecha', 'horas'), 'descripcion', 'observaciones')}),)
    list_display = ('maquina', 'fecha', 'horas')
    list_filter = ('maquina',)
    # inlines = [SalidaMMEDInline,]


admin.site.register(Existencias, ExistenciasAdmin)
admin.site.register(Personal)
admin.site.register(Plantel)
admin.site.register(Instalacion)
admin.site.register(PersonalP)
admin.site.register(Material, MaterialAdmin)
admin.site.register(RegistroMaquinas, RegistroMaquinasAdmin)
admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Ingresos, IngresosAdmin)
admin.site.register(Salida, SalidaAdmin)
admin.site.register(SalidaOT)
admin.site.register(MaterialMantenimiento, MMantoAdmin)
admin.site.register(MaterialMaquina, MMQAdmin)
admin.site.register(Ot, OTAdmin)
admin.site.register(MantPreventivo, PrevManto)
actions.add_to_site(admin.site)
admin.site.register(MantPreventivoOT, MantPrevOTAdmin)
# Register your models here.
