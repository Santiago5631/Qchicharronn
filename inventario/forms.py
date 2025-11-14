from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import InventarioDiario, MovimientoInventario
from producto.models import Producto
from decimal import Decimal


class AperturaInventarioForm(forms.ModelForm):
    """Formulario para abrir el inventario del día"""

    class Meta:
        model = InventarioDiario
        fields = ['fecha', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones del día (opcional)...'
            }),
        }
        labels = {
            'fecha': 'Fecha del Inventario',
            'observaciones': 'Observaciones',
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # Ya no bloquea inventarios del mismo día, solo valida formato o existencia del valor
        if not fecha:
            raise forms.ValidationError("Debe seleccionar una fecha válida.")
        return fecha


class MovimientoInventarioForm(forms.ModelForm):
    """Formulario para registrar el inventario inicial de cada producto"""

    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'inventario_inicial']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'inventario_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
        }
        labels = {
            'producto': 'Producto',
            'inventario_inicial': 'Inventario Inicial',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya existe el producto, prellenar con el stock actual
        if self.instance and self.instance.pk is None:
            if 'producto' in self.initial:
                try:
                    producto = Producto.objects.get(pk=self.initial['producto'])
                    self.initial['inventario_inicial'] = producto.stock
                except Producto.DoesNotExist:
                    pass


class CierreInventarioForm(forms.ModelForm):
    """Formulario para registrar el inventario final (cierre del día)"""

    class Meta:
        model = MovimientoInventario
        fields = ['inventario_final', 'motivo_ajuste']
        widgets = {
            'inventario_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True,
            }),
            'motivo_ajuste': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Merma, rotura, error de conteo...',
            }),
        }
        labels = {
            'inventario_final': 'Inventario Final (Físico)',
            'motivo_ajuste': 'Motivo del Ajuste (si aplica)',
        }

    def clean_inventario_final(self):
        inventario_final = self.cleaned_data.get('inventario_final')
        if inventario_final is None:
            raise forms.ValidationError("Debe ingresar el inventario final")
        if inventario_final < 0:
            raise forms.ValidationError("El inventario no puede ser negativo")
        return inventario_final


# Formset para múltiples productos en la apertura
MovimientoInventarioFormSet = modelformset_factory(
    MovimientoInventario,
    form=MovimientoInventarioForm,
    extra=0,
    can_delete=False,
)

# Formset para el cierre de inventario
CierreInventarioFormSet = modelformset_factory(
    MovimientoInventario,
    form=CierreInventarioForm,
    extra=0,
    can_delete=False,
)


class AjusteInventarioForm(forms.Form):
    """Formulario para ajustes manuales de inventario"""
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(disponible=True),
        label='Producto',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_movimiento = forms.ChoiceField(
        choices=[
            ('entrada', 'Entrada (Suma)'),
            ('salida', 'Salida (Resta)'),
            ('ajuste', 'Ajuste (Corrección)'),
        ],
        label='Tipo de Movimiento',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label='Cantidad',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    motivo = forms.CharField(
        max_length=200,
        required=True,
        label='Motivo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Explique el motivo del ajuste...'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        tipo_movimiento = cleaned_data.get('tipo_movimiento')
        cantidad = cleaned_data.get('cantidad')

        # Validar que no se reste más de lo disponible
        if tipo_movimiento == 'salida' and producto:
            if producto.stock < cantidad:
                raise forms.ValidationError(
                    f"No hay suficiente stock. Disponible: {producto.stock}"
                )

        return cleaned_data


class FiltroReporteForm(forms.Form):
    """Formulario para filtrar reportes de inventario"""
    fecha_desde = forms.DateField(
        required=False,
        label='Desde',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        label='Hasta',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        label='Producto',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label='Todos los productos'
    )
    tipo_control = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Todos'),
            ('peso', 'Por Peso'),
            ('unidad', 'Por Unidad'),
        ],
        label='Tipo de Control',
        widget=forms.Select(attrs={'class': 'form-control'})
    )