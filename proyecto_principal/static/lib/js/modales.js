// ===== FUNCIONES GLOBALES PARA MODALES =====
function abrirModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        // Pequeño delay para la animación
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);
    }
}

function cerrarModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }, 300);
    }
}

// Cerrar modal al hacer clic fuera del contenido
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('simple-modal')) {
        const modalId = e.target.id;
        cerrarModal(modalId);
    }
});

// Cerrar modal con tecla ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.simple-modal');
        modals.forEach(modal => {
            if (modal.style.display === 'block') {
                cerrarModal(modal.id);
            }
        });
    }
});

// ===== FUNCIÓN PARA MOSTRAR MENSAJES DINÁMICOS =====
function mostrarMensaje(tipo, texto) {
    const container = document.getElementById('messages-container');
    if (!container) {
        console.error('No se encontró el contenedor de mensajes');
        return;
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${tipo}`;
    msgDiv.textContent = texto;

    container.appendChild(msgDiv);

    setTimeout(() => {
        msgDiv.style.opacity = '0';
        setTimeout(() => msgDiv.remove(), 500);
    }, 3000);
}