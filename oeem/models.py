#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

class Plantel(models.Model):
    ciudad = models.CharField(max_length=20, verbose_name='Lugar')

    class Meta:
        verbose_name = 'Plantel'
        verbose_name_plural = 'Planteles'

    def __str__(self):
        return '%s' % (self.ciudad)

class Instalacion(models.Model):
    ubicacion = models.ForeignKey(Plantel, verbose_name='Lugar')
    asignado = models.CharField(max_length=35, verbose_name='Ubicación')


    def __str__(self):
        return '%s, %s' % (self.ubicacion, self.asignado)

    class Meta:
        verbose_name = 'Instalación'
        verbose_name_plural = 'Instalaciones'

class Maquina(models.Model):
    descripcion = models.CharField(max_length=30, verbose_name='Descripcion')
    modelo = models.CharField(max_length=18, verbose_name='Modelo')
    marca = models.CharField(max_length=18, verbose_name='Marca')
    
    def __str__(self):
        return '%s, %s' % (self.descripcion, self.modelo)
    
    class Meta:
        verbose_name = 'Catálogo de Máquinas'
        verbose_name_plural = 'Catálogo de Maquinas'
        
class Instalaciones(models.Model):
    descripcion=models.CharField(max_length=30, verbose_name='Descripcion')
    dpt=(('m', 'Mantenimiento'), ('p', 'Produccion'), ('l', 'Logística'), ('c', 'Calidad'), ('r', 'RRHH'), ('a', 'Contabilidad'), ('f', 'Auditoría'), ('v', 'Ventas'), ('b', 'Compras'),) 
    
class Material(models.Model):
    descripcion = models.CharField(max_length=50, verbose_name='Descripcion de Material o Repuesto')
    partnumber = models.CharField(max_length=20, verbose_name='Codigo/Numero de parte')
    
    def __str__(self):
        return '%s, %s' % (self.descripcion, self.partnumber)
    
    class Meta:
        verbose_name = 'Catálogo de Repuestos y Materiales'
        verbose_name_plural = 'Catálogo de Repuestos y Materiales'
    
class Personal(models.Model):
    nombre = models.CharField(max_length=20, verbose_name='Nombre')
    
    def __str__(self):
        return '%s' % (self.nombre)
    
    class Meta:
        verbose_name = 'Personal de Mantenimiento'
        verbose_name_plural = 'Personal de Mantenimiento'
        
class RegistroMaquinas(models.Model):
    codigo = models.CharField(max_length=8, verbose_name='Codigo')
    maquina = models.ForeignKey(Maquina, verbose_name='Maquinas', on_delete=models.CASCADE)
    horas = models.PositiveSmallIntegerField(verbose_name='Horas de operacion')
    serie = models.CharField(max_length=18, verbose_name='Serie')
    area = models.CharField(max_length=12, verbose_name='Area Asignada', choices=(('r', 'Sala de Maquinas'), ('c', 'Produccion Cerdo'), ('e', 'Produccion Embutidos'), ('v', 'Produccion Res'), ('f','Flota'), ('d', 'Despacho'), ('p', 'Planta Tratamiento')), default='c')
    ubicacion = models.ForeignKey(Instalacion, verbose_name='Ubicacion', null=True)

    def __str__(self):
        return '%s, %s, %s' % (self.codigo, self.maquina, self.ubicacion)
    
    class Meta:
        verbose_name = 'Registro de Maquinaria y Equipos'
        verbose_name_plural = 'Registro de Maquinaria y Equipos'
        order_with_respect_to = 'maquina'

    def save(self, *args, **kwargs):
        super(RegistroMaquinas, self).save(*args, **kwargs)
        self.update()
        
    def update(self):
        try:
            upd = MantPreventivo.objects.get(maquina = self.id)
            upd.hours = upd.nhours - self.horas
            if (upd.hours<= 100) and (upd.hours>0):
                upd.status = 'p'
            elif upd.hours <= 0:
                upd.status = 'r'
            else:
                upd.status = 'c'
            upd.save()
        except MantPreventivo.DoesNotExist:
            pass

class PersonalP(models.Model):
    nombre = models.CharField(max_length=20, verbose_name='Nombre')
    
    def __str__(self):
        return '%s' % (self.nombre)
    
    class Meta:
        verbose_name = 'Personal de Produccion'
        verbose_name_plural = 'Personal de Produccion'


class MaterialMaquina(models.Model):
    material = models.ForeignKey(Material, verbose_name='Material o Repuesto', on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, verbose_name='Maquina', on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField(default='1')
    
    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'
    
    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'),(Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)
    
    def __str__(self):
        return '%s' % (self.material)
    
    class Meta:
        verbose_name = 'Catalogo de Repuestos'
        verbose_name_plural = 'Catalogo de Repuestos de Maquinas'

class Existencias(models.Model):
    material = models.ForeignKey(Material, verbose_name='Material')
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad', default='1')
    
    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'
    
    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'),(Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)
    ubicacion = models.CharField(verbose_name='ubicacion', max_length=30)
    
    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario de Repuestos y Materiales'

class Ingresos(models.Model):
    material = models.ForeignKey(Material, verbose_name='Material')
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad ingresada', default='1')
    fecha = models.DateField(verbose_name='Fecha de ingreso')
    receptor = models.ForeignKey(Personal, verbose_name='Recibido por')
    
    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'
    
    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'),(Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)
    
    class Meta:
        verbose_name = 'Ingreso de Repuestos y Materiales'
        verbose_name_plural = 'Registro de Ingresos de Repuestos y Materiales'
        
    def save(self, *args, **kwargs):
        super(Ingresos, self).save(*args, **kwargs)
        self.update()
        
    def update(self):
        try:
            cantidad1 = Existencias.objects.get(material=self.material)
        except Existencias.DoesNotExist:
            cantidad1 = Existencias(material=self.material, cantidad=0)
            cantidad1.save()
        cantidad2 = Ingresos.objects.get(id = self.id)
        cantidad1.cantidad = cantidad1.cantidad + self.cantidad
        cantidad1.save()

class Salida(models.Model):
    material = models.ForeignKey(Material, verbose_name='Material o Repuesto')
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad Entregada', default='1')
    fecha = models.DateField(verbose_name='Fecha')
    receptor = models.ForeignKey(Personal, verbose_name='Instalada por')
    horas = models.PositiveSmallIntegerField(verbose_name='Horas de trabajo de la máquina',  default='0')
    maquina = models.ForeignKey(RegistroMaquinas, verbose_name='Maquina', blank=True, null=True)
    
    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'
    
    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'),(Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)
    
    
    class Meta:
        verbose_name = 'Salida de Repuestos y Materiales'
        verbose_name_plural = 'Registro de Salidas de Repuestos y Materiales'
        
    def save(self, *args, **kwargs):
        super(Salida, self).save(*args, **kwargs)
        self.update()
        
    def update(self):
        try:
            ver = Salida.objects.get(id=self.id)
        except:
            cantidad1 = Existencias.objects.get(material=self.material)
            cantidad2 = Salida.objects.get(id = self.id)
            cantidad1.cantidad = cantidad1.cantidad - self.cantidad
            cantidad1.save()

class MantPreventivo(models.Model):
    tarea = models.CharField(max_length=50, verbose_name='Tarea')
    maquina = models.ForeignKey(RegistroMaquinas, verbose_name='Equipo')

    diario = '1'
    semanal = '7'
    mensual = '30'
    tri = '90'
    semtral = '180'
    anual = '365'

    rango = (
        (diario, 'Diario'), (semanal, 'Semanal'), (mensual, 'Mensual'), (tri, 'Trimestral'), (semtral, 'Semestral'),
        (anual, 'Anual'),)
    intervalo = models.CharField(verbose_name='Intervalo Dias', choices=rango, default='7', max_length=10)
    lapso = models.PositiveSmallIntegerField(verbose_name='Intervalo Horas', default=0)
    ldate = models.DateField(verbose_name='Ultimo Mantenimiento', blank=True, null=True)
    lhours = models.PositiveSmallIntegerField(verbose_name='Horas Ultimo Mantenimiento', default=0, blank=True, null=True)
    nhours = models.PositiveSmallIntegerField(verbose_name='Horas Proximo Mantenimiento', default=0, blank=True, null=True)
    ndate = models.DateField(verbose_name='Proximo Mantenimiento', blank=True, null=True)
    status = models.CharField(max_length=10, verbose_name='Estado', choices=(('p', 'Pendiente'), ('c', 'En Orden'), ('r', 'Retrasado')), default='r')
    descripcion = models.TextField(verbose_name='Descripcion')
    hours = models.PositiveSmallIntegerField(default=0, verbose_name='Horas Restantes')

    def __str__(self):
        return '%s' % (self.tarea)

    class Meta:
        verbose_name='Programacion Mantenimiento Preventivo'
        verbose_name_plural = 'Programacion Mantenimiento Preventivo'

class Ot(models.Model):
    idn = models.AutoField(verbose_name='Número', primary_key=True, unique=True)
    maquina = models.ForeignKey(RegistroMaquinas, verbose_name='Maquina')
    dpto = (('m', 'Mantenimiento'),('l', 'Logística'), ('p', 'Produccion'), ('c', 'Calidad'), ('v', 'Ventas'), ('o', 'Otros'),)
    departamento = models.CharField(verbose_name='Departamento', choices=dpto, max_length=1)
    rel = (('c', 'Calidad'), ('i', 'Inocuidad'), ('o', 'Operación'), ('e', 'Eficiencia'), ('s', 'Seguridad'),)
    relacionado = models.CharField(verbose_name='Incidencia', choices=rel, max_length=1, default='o')
    crit = (('a', 'Alta'), ('m', 'Media'), ('b', 'Moderada'))
    criticidad = models.CharField(verbose_name='Criticidad', choices=crit, max_length=1, default='b')
    sel = (('p', 'Mantenimiento Preventivo'), ('c', 'Mantenimiento Correctivo'), ('l', 'Limpieza'),)
    tipo = models.CharField(verbose_name='Tipo', choices=sel, max_length=1, default='c')
    asignado = models.ForeignKey(Personal, verbose_name='Asignado a', null=True)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha = models.DateTimeField(verbose_name='Fecha', auto_now_add=True)
    solicita = models.ForeignKey(User, verbose_name='Solicitado por', null=True)
    status = models.CharField(choices=(('p', 'Abierta'), ('c', 'Cerrada'), ('s', 'Stand-By')), default='p', verbose_name='Estado', max_length=1)
    prog = models.DateField(verbose_name='Fecha Programada', blank=True, null=True)
    cierre = models.DateField(verbose_name='Fecha de Cierre', blank=True, null=True)
    mantoid = models.PositiveSmallIntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name='Orden de Trabajo'
        verbose_name_plural='Órdenes de Trabajo'

class CerrarOt(models.Model):
    ot = models.OneToOneField(Ot, verbose_name='Orden de Trabajo')
    tiempo = models.PositiveSmallIntegerField(verbose_name='Tiempo de Ejecucion')
    fin = models.DateTimeField(verbose_name='Fecha de Finalizacion')
    ejecucion = models.TextField(verbose_name='Trabajo realizado')
    observaciones = models. TextField(verbose_name='Observaciones')
    horas = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    inicio = models.DateTimeField(verbose_name='Fecha de Inicio', null=True)
    cierre = models.DateField(verbose_name='Fecha de Cierre', null=True)

    class Meta:
        verbose_name='Cierre de Orden de Trabajo'
        verbose_name_plural='Cierres de Ordenes de Trabajo'
        permissions = (
            ('view_cerrarot', 'Can View CerrarOt'),
        )

    def save(self, *args, **kwargs):
        super(CerrarOt, self).save(*args, **kwargs)
        self.update()

    def update(self):
        cot = CerrarOt.objects.get(id=self.id)
        numot = Ot.objects.get(idn=cot.ot_id)
        numot.cierre = self.cierre
        numot.status = str('c')
        print (numot.mantoid)
        if numot.mantoid != 0:
            print ('OK')
            manto = MantPreventivo.objects.get(id=numot.mantoid)
            manto.ldate = self.fin
            manto.lhours = self.horas
            manto.ndate = datetime.timedelta(int(manto.intervalo)) + self.fin
            MantPreventivoOT.objects.create(ot=self.ot, prev=manto, tiempo=self.tiempo, maquina=numot.maquina, horas=self.horas, fecha=self.fin, descripcion=self.ejecucion, observaciones=self.observaciones)
            if self.horas != 0:
                manto.nhours = self.horas + manto.lapso
            manto.save()

        else:
            pass
        numot.save()

class MantPreventivoOT(models.Model):
    prev = models.ForeignKey(MantPreventivo, verbose_name='Tarea')
    tiempo = models.PositiveSmallIntegerField(verbose_name='Tiempo de ejecución')
    maquina = models.ForeignKey(RegistroMaquinas, verbose_name='Maquina', blank=True, null=True, default=1)
    horas = models.IntegerField(verbose_name='Horas', blank=True)
    fecha = models.DateField(verbose_name='Fecha')
    descripcion = models.TextField(verbose_name='Trabajo Realizado', blank=True, null=True, max_length=1000)
    observaciones = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    ot = models.ForeignKey(Ot, verbose_name='Orden de Trabajo', null=True)
    horas = models.PositiveSmallIntegerField(default=0, verbose_name='Horas')

    def __str__(self):
        return '%s' % (self.prev)

    class Meta:
        verbose_name = 'Ejecución de Mantenimiento Preventivo'
        verbose_name_plural = 'Ejecución de Mantenimientos Preventivos'

class SalidaOT(models.Model):
    uso = models.ForeignKey(Ot, verbose_name='Usado en', null=True, blank=True)
    material = models.ForeignKey(Material, verbose_name='Material o Repuesto')
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad Entregada', default='1')
    fecha = models.DateField(verbose_name='Fecha')
    receptor = models.ForeignKey(Personal, verbose_name='Instalada por')
    horas = models.PositiveSmallIntegerField(verbose_name='Horas de trabajo de la máquina', default='0')
    maquina = models.ForeignKey(RegistroMaquinas, verbose_name='Maquina', blank=True, null=True)

    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'

    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'), (Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)

    class Meta:
        verbose_name = 'Salida de Repuestos y Materiales'
        verbose_name_plural = 'Registro de Salidas de Repuestos y Materiales'

    def save(self, *args, **kwargs):
        super(SalidaOT, self).save(*args, **kwargs)
        self.update()

    def update(self):
        try:
            ver = Salida.objects.get(id=self.id)
        except:
            cantidad1 = Existencias.objects.get(material=self.material)
            cantidad2 = SalidaOT.objects.get(id=self.id)
            cantidad1.cantidad = cantidad1.cantidad - self.cantidad
            cantidad1.save()


class MaterialMantenimiento(models.Model):
    manto = models.ForeignKey(MantPreventivo, verbose_name='Mantenimiento Asociado')
    materiales = models.ForeignKey(MaterialMaquina, verbose_name='Materiales Necesarios')
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad Requerida', default='1')
    
    Gal = 'g'
    Uni = 'u'
    Lib = 'p'
    Par = 't'
    Lit = 'l'
    Doc = 'd'
    Qt = 'q'
    Cil = 'c'
    Tub = 'b'
    Bot = 'a'
    
    unit = (
        (Gal, 'Galones'), (Uni, 'Unidades'), (Lib, 'Libras'), (Par, 'Pares'), (Lit, 'Litros'),
        (Doc, 'Docenas'), (Qt, 'Cuartos'), (Cil, 'Cilindros'), (Tub, 'Tubos'),(Bot, 'Botes'),)
    unidad = models.CharField(verbose_name='Unidad Medida', choices=unit, default='u', max_length=10)
    
    def __str__(self):
        return '%s' % (self.materiales)
    
    class Meta:
        verbose_name = 'Materiales para Mantenimiento'
        verbose_name_plural = 'Materiales para Mantenimiento'