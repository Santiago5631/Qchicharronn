from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random

# ── modelos ──────────────────────────────────────────────────────────────────
from categoria.models import Categoria
from marca.models import Marca
from proveedor.models import Proveedor
from unidad.models import Unidad
from producto.models import Producto
from mesa.models import Mesa
from menu.models import Menu, MenuProducto, Pedido, PedidoItem
from venta.models import Venta, VentaItem

try:
    from clientes.models import Cliente
    TIENE_CLIENTES = True
except ImportError:
    TIENE_CLIENTES = False

User = get_user_model()

# ── datos de ejemplo ──────────────────────────────────────────────────────────
NOMBRES_CLIENTES = [
    "Carlos Ramírez", "Laura Gómez", "Andrés Torres", "Sofía Herrera",
    "Miguel Ángel Peña", "Isabella Vargas", "Sebastián Morales", "Valentina Cruz",
    "Daniel Ortiz", "Camila Jiménez", "Juan Pablo Ríos", "María José Castillo",
    "Felipe Mendoza", "Ana Lucía Paredes", "Diego Salcedo", "Natalia Bermúdez",
    "Alejandro Suárez", "Gabriela Niño", "Esteban Lozano", "Paola Acevedo",
    "Julián Cárdenas", "Mariana Pinto", "Ricardo Bernal", "Sandra Velásquez",
    "Mauricio Ospina", "Claudia Restrepo", "Hernán Arango", "Patricia Duarte",
    "Gustavo Pedraza", "Liliana Montoya", "Nelson Castaño", "Gloria Zea",
    "Armando Quiroga", "Esperanza Téllez", "Rodrigo Fonseca", "Beatriz Leal",
]

NOMBRES_MENUS = [
    "Bandeja Paisa", "Chicharrón Especial", "Ajiaco Bogotano", "Sancocho de Gallina",
    "Fritanga Mixta", "Picada Colombiana", "Costillas BBQ", "Chuleta de Cerdo",
    "Morcilla con Arepa", "Longaniza Asada", "Combo Familiar", "Medio Combo",
    "Porción Chicharrón", "Plato Ejecutivo", "Menú del Día",
    "Bandeja Vegetariana", "Sopa del Día", "Ensalada Tropical", "Arroz con Pollo",
    "Filete de Res", "Pechuga a la Plancha", "Trucha al Ajillo",
    "Caldo de Costilla", "Mondongo Especial", "Hervido de Res",
]

NOMBRES_PRODUCTOS = [
    ("Chicharrón de Cerdo", "plato"), ("Costilla de Cerdo", "plato"),
    ("Morcilla", "plato"), ("Longaniza", "plato"), ("Chuleta", "plato"),
    ("Pollo Asado", "plato"), ("Res Molida", "plato"), ("Lomo de Res", "plato"),
    ("Arroz Blanco", "plato"), ("Frijoles", "plato"), ("Papa Criolla", "plato"),
    ("Arepa de Maíz", "plato"), ("Patacón", "plato"), ("Yuca Frita", "plato"),
    ("Ensalada Verde", "plato"), ("Aguacate", "plato"), ("Huevo Frito", "plato"),
    ("Chorizo", "plato"), ("Bandeja Especial", "plato"), ("Trucha", "plato"),
    ("Aceite Vegetal", "venta"), ("Sal", "venta"), ("Azúcar", "venta"),
    ("Harina de Maíz", "venta"), ("Condimentos Mix", "venta"),
    ("Salsa de Tomate", "venta"), ("Ají Picante", "venta"),
    ("Mantequilla", "venta"), ("Leche", "venta"), ("Queso Campesino", "venta"),
]

UBICACIONES_MESA = ["Zona A - Interior", "Zona B - Terraza", "Zona C - VIP", "Zona D - Bar"]

AREAS = ["parrilla", "cocina"]
METODOS_PAGO = ["efectivo", "tarjeta", "transferencia"]
ESTADOS_PEDIDO = ["entregado", "cancelado"]
ESTADOS_VENTA = ["pagado", "anulada"]
TIPOS_PEDIDO = ["mesa", "llevar"]


class Command(BaseCommand):
    help = "Pobla la base de datos con 1.000+ registros de prueba"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina los datos de prueba antes de crear nuevos',
        )
        parser.add_argument(
            '--pedidos', type=int, default=300,
            help='Número de pedidos a crear (default: 300)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n══════════════════════════════════════'))
        self.stdout.write(self.style.WARNING('   POBLADOR DE BASE DE DATOS'))
        self.stdout.write(self.style.WARNING('══════════════════════════════════════\n'))

        if options['limpiar']:
            self._limpiar()

        # ── Paso 1: dependencias base ─────────────────────────────────────
        self.stdout.write('📦 Creando dependencias base...')
        categorias = self._crear_categorias()
        marcas = self._crear_marcas()
        proveedores = self._crear_proveedores()
        unidades = self._crear_unidades()
        usuario = self._obtener_o_crear_usuario()

        # ── Paso 2: entidades principales ────────────────────────────────
        self.stdout.write('🪑 Creando mesas...')
        mesas = self._crear_mesas()

        self.stdout.write('🥩 Creando productos...')
        productos = self._crear_productos(categorias, marcas, proveedores, unidades)

        self.stdout.write('📋 Creando menús...')
        menus = self._crear_menus(categorias, productos)

        # ── Paso 3: clientes ──────────────────────────────────────────────
        clientes = self._crear_clientes() if TIENE_CLIENTES else []

        # ── Paso 4: pedidos + ventas ──────────────────────────────────────
        n_pedidos = options['pedidos']
        self.stdout.write(f'🛒 Creando {n_pedidos} pedidos y sus ventas...')
        self._crear_pedidos_y_ventas(n_pedidos, menus, mesas, usuario, clientes)

        # ── Resumen ───────────────────────────────────────────────────────
        self._imprimir_resumen()

    # =========================================================================
    # LIMPIEZA
    # =========================================================================
    def _limpiar(self):
        self.stdout.write(self.style.ERROR('🗑  Limpiando datos de prueba...'))
        VentaItem.objects.all().delete()
        Venta.objects.all().delete()
        PedidoItem.objects.all().delete()
        Pedido.objects.all().delete()
        MenuProducto.objects.all().delete()
        Menu.objects.all().delete()
        Producto.objects.all().delete()
        Mesa.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('   ✓ Limpieza completada\n'))

    # =========================================================================
    # DEPENDENCIAS BASE
    # =========================================================================
    def _crear_categorias(self):
        nombres = [
            "Carnes", "Acompañamientos", "Sopas", "Ensaladas",
            "Bebidas", "Postres", "Parrilla", "Cocina Tradicional",
            "Vegetariano", "Mariscos",
        ]
        cats = []
        for nombre in nombres:
            obj, _ = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': f'Categoría {nombre}'}
            )
            cats.append(obj)
        self.stdout.write(f'   ✓ {len(cats)} categorías')
        return cats

    def _crear_marcas(self):
        datos = [
            ("Zenú", "Colombia"), ("Rica", "Colombia"), ("Colanta", "Colombia"),
            ("Alpina", "Colombia"), ("Noel", "Colombia"), ("Quala", "Colombia"),
        ]
        marcas = []
        for nombre, pais in datos:
            obj, _ = Marca.objects.get_or_create(
                nombre=nombre,
                defaults={'pais_origen': pais, 'descripcion': f'Marca {nombre}'}
            )
            marcas.append(obj)
        self.stdout.write(f'   ✓ {len(marcas)} marcas')
        return marcas

    def _crear_proveedores(self):
        datos = [
            ("900123456-1", "Carnes del Llano"),
            ("900234567-2", "Distribuidora Central"),
            ("900345678-3", "Frigorífico Nacional"),
            ("900456789-4", "Abastos Boyacá"),
        ]
        proveedores = []
        for nit, nombre in datos:
            obj, _ = Proveedor.objects.get_or_create(
                nit=nit,
                defaults={'nombre': nombre}
            )
            proveedores.append(obj)
        self.stdout.write(f'   ✓ {len(proveedores)} proveedores')
        return proveedores

    def _crear_unidades(self):
        datos = [
            ("Kilogramo", "kg", "peso"),
            ("Gramo", "g", "peso"),
            ("Litro", "L", "peso"),
            ("Unidad", "und", "unidad"),
            ("Porción", "por", "unidad"),
        ]
        unidades = []
        for nombre, desc, tipo in datos:
            obj, _ = Unidad.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'tipo': tipo}
            )
            unidades.append(obj)
        self.stdout.write(f'   ✓ {len(unidades)} unidades')
        return unidades

    def _obtener_o_crear_usuario(self):
        user = User.objects.filter(is_active=True).first()
        if not user:
            user = User.objects.create_user(
                username='mesero_prueba',
                password='Test1234!',
                first_name='Mesero',
                last_name='Prueba',
            )
            self.stdout.write('   ✓ Usuario mesero_prueba creado (pass: Test1234!)')
        else:
            self.stdout.write(f'   ✓ Usando usuario existente: {user.username}')
        return user

    # =========================================================================
    # MESAS
    # =========================================================================
    def _crear_mesas(self):
        mesas = []
        numero_inicio = Mesa.objects.count() + 1
        for i in range(numero_inicio, numero_inicio + 30):
            obj, created = Mesa.objects.get_or_create(
                numero=str(i),
                defaults={
                    'capacidad': random.choice([2, 4, 4, 6, 8]),
                    'ubicacion': random.choice(UBICACIONES_MESA),
                }
            )
            mesas.append(obj)
        self.stdout.write(f'   ✓ {Mesa.objects.count()} mesas totales')
        return list(Mesa.objects.all())

    # =========================================================================
    # PRODUCTOS
    # =========================================================================
    def _crear_productos(self, categorias, marcas, proveedores, unidades):
        creados = 0
        for nombre, tipo_uso in NOMBRES_PRODUCTOS:
            obj, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'marca': random.choice(marcas),
                    'categoria': random.choice(categorias),
                    'proveedor': random.choice(proveedores),
                    'unidad': random.choice(unidades),
                    'tipo_uso': tipo_uso,
                    'stock': Decimal(str(round(random.uniform(10, 500), 2))),
                    'area_preparacion': random.choice(AREAS),
                    'disponible': True,
                }
            )
            if created:
                creados += 1

        productos = list(Producto.objects.filter(disponible=True))
        self.stdout.write(f'   ✓ {len(productos)} productos totales ({creados} nuevos)')
        return productos

    # =========================================================================
    # MENÚS
    # =========================================================================
    def _crear_menus(self, categorias, productos):
        creados = 0
        productos_plato = [p for p in productos if p.tipo_uso == 'plato']
        if not productos_plato:
            productos_plato = productos

        for nombre in NOMBRES_MENUS:
            obj, created = Menu.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': f'Delicioso {nombre} preparado con ingredientes frescos',
                    'categoria_menu': random.choice(categorias),
                    'precio_base': Decimal(str(random.randint(12, 65) * 1000)),
                    'descuento': Decimal(str(random.choice([0, 0, 0, 5, 10]))),
                    'disponible': True,
                }
            )
            if created:
                creados += 1
                # Agregar entre 2 y 5 productos al menú
                muestra = random.sample(productos_plato, min(random.randint(2, 5), len(productos_plato)))
                for idx, prod in enumerate(muestra):
                    MenuProducto.objects.get_or_create(
                        menu=obj,
                        producto=prod,
                        defaults={'cantidad': Decimal(str(random.randint(1, 3))), 'orden': idx}
                    )

        menus = list(Menu.objects.filter(disponible=True))
        self.stdout.write(f'   ✓ {len(menus)} menús totales ({creados} nuevos)')
        return menus

    # =========================================================================
    # CLIENTES
    # =========================================================================
    def _crear_clientes(self):
        clientes = []
        for i, nombre in enumerate(NOMBRES_CLIENTES):
            partes = nombre.split()
            obj, _ = Cliente.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'numero_documento': str(1000000000 + i),
                }
            )
            clientes.append(obj)
        self.stdout.write(f'   ✓ {len(clientes)} clientes')
        return clientes

    # =========================================================================
    # PEDIDOS + VENTAS  (núcleo: genera el grueso de los registros)
    # =========================================================================
    def _crear_pedidos_y_ventas(self, n_pedidos, menus, mesas, usuario, clientes):
        if not menus:
            self.stdout.write(self.style.ERROR('   ✗ No hay menús disponibles, abortando'))
            return

        pedidos_creados = 0
        ventas_creadas = 0

        for i in range(n_pedidos):
            # ── datos base del pedido ─────────────────────────────────────
            tipo = random.choice(TIPOS_PEDIDO)
            mesa = random.choice(mesas) if tipo == 'mesa' and mesas else None
            nombre_cliente = random.choice(NOMBRES_CLIENTES)
            estado_pedido = random.choice(ESTADOS_PEDIDO)

            # ── crear pedido ──────────────────────────────────────────────
            pedido = Pedido(
                cliente_nombre=nombre_cliente,
                tipo_pedido=tipo,
                mesero=usuario,
                mesa=mesa,
                estado=estado_pedido,
                observaciones=random.choice([
                    '', '', '', 'Sin picante', 'Extra salsa', 'Sin cebolla',
                    'Para llevar bien empacado', 'Urgente'
                ]),
            )
            pedido.save()  # genera numero_pedido automático

            # ── agregar ítems al pedido ───────────────────────────────────
            menus_elegidos = random.sample(menus, random.randint(1, min(4, len(menus))))
            subtotal = Decimal('0')
            descuento_total = Decimal('0')

            items_pedido = []
            for menu in menus_elegidos:
                cantidad = random.randint(1, 3)
                precio = menu.precio_base
                descuento = menu.descuento

                item = PedidoItem(
                    pedido=pedido,
                    menu=menu,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    descuento_aplicado=descuento,
                )
                items_pedido.append(item)
                sub = precio * cantidad
                desc = sub * (descuento / 100)
                subtotal += sub
                descuento_total += desc

            PedidoItem.objects.bulk_create(items_pedido)

            total = subtotal - descuento_total
            pedido.subtotal = subtotal
            pedido.descuento_total = descuento_total
            pedido.total = total
            pedido.save()
            pedidos_creados += 1

            # ── crear venta solo para pedidos entregados ──────────────────
            if estado_pedido == 'entregado':
                cliente_obj = random.choice(clientes) if clientes else None
                estado_venta = random.choice(ESTADOS_VENTA)

                venta = Venta(
                    cliente=cliente_obj,
                    cliente_factura=cliente_obj,
                    mesero=usuario,
                    metodo_pago=random.choice(METODOS_PAGO),
                    pedido=pedido,
                    cliente_nombre=nombre_cliente,
                    tipo_pedido=tipo,
                    mesa=mesa,
                    subtotal=subtotal,
                    descuento_total=descuento_total,
                    total=total,
                    estado=estado_venta,
                )
                venta.save()  # genera numero_factura automático

                # ── ítems de la venta ─────────────────────────────────────
                items_venta = []
                for item in items_pedido:
                    items_venta.append(VentaItem(
                        venta=venta,
                        nombre=item.menu.nombre if item.menu else 'Ítem',
                        cantidad=item.cantidad,
                        precio_unitario=item.precio_unitario,
                        subtotal=item.precio_unitario * item.cantidad,
                    ))
                VentaItem.objects.bulk_create(items_venta)
                ventas_creadas += 1

            # ── progreso cada 50 registros ────────────────────────────────
            if (i + 1) % 50 == 0:
                self.stdout.write(f'   ... {i + 1}/{n_pedidos} pedidos procesados')

        self.stdout.write(self.style.SUCCESS(
            f'   ✓ {pedidos_creados} pedidos creados, {ventas_creadas} ventas creadas'
        ))

    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    def _imprimir_resumen(self):
        self.stdout.write('\n' + self.style.SUCCESS('══════════════════════════════════════'))
        self.stdout.write(self.style.SUCCESS('   RESUMEN FINAL'))
        self.stdout.write(self.style.SUCCESS('══════════════════════════════════════'))

        modelos = [
            ('Mesas',     Mesa.objects.count()),
            ('Categorías', Categoria.objects.count()),
            ('Productos', Producto.objects.count()),
            ('Menús',     Menu.objects.count()),
            ('Pedidos',   Pedido.objects.count()),
            ('Ventas',    Venta.objects.count()),
        ]

        total = 0
        for nombre, count in modelos:
            indicador = '✅' if count >= 30 else '⚠️ '
            self.stdout.write(f'   {indicador}  {nombre:<15} {count:>6} registros')
            total += count

        self.stdout.write(self.style.SUCCESS(f'\n   TOTAL GENERAL:    {total:>6} registros'))
        self.stdout.write(self.style.SUCCESS('══════════════════════════════════════\n'))