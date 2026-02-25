from django import forms
from .models import Nomina
from usuario.models import Usuario


class NominaForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(estado='activo'),
        label='Empleado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    fecha_inicio = forms.DateField(
        label='Fecha Inicio',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d']
    )

    fecha_fin = forms.DateField(
        label='Fecha Fin',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d']
    )

    fecha_pago = forms.DateField(
        label='Fecha de Pago',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Nomina
        fields = ['empleado', 'tipo_pago', 'valor_unitario', 'cantidad',
                  'fecha_inicio', 'fecha_fin', 'fecha_pago', 'estado', 'observaciones']
        widgets = {
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'empleado': 'Empleado',
            'tipo_pago': 'Tipo de Pago',
            'valor_unitario': 'Valor por Hora/Día',
            'cantidad': 'Horas/Días Trabajados',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }


class NominaFiltroForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha Inicio'
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha Fin'
    )
    empleado = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(estado='activo'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Empleado',
        empty_label='Todos los empleados'
    )
    estado = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + Nomina.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Estado'
    )

