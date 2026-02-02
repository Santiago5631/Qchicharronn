(function($) {
  "use strict"; // Start of use strict

  // ============================================================
  // TOGGLE SIDEBAR - ADAPTADO PARA DESKTOP Y MÓVIL
  // ============================================================

  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    e.preventDefault();

    // Para pantallas grandes (>900px): Toggle colapsado/expandido
    if ($(window).width() > 900) {
      $("body").toggleClass("sidebar-toggled");
      $("#accordionSidebar").toggleClass("toggled");

      // Cerrar todos los collapse cuando se colapsa
      if ($("#accordionSidebar").hasClass("toggled")) {
        $('#accordionSidebar .collapse').collapse('hide');
      }
    }
    // Para móvil (≤900px): Mostrar/ocultar sidebar con .show
    else {
      $("#accordionSidebar").toggleClass("show");

      // Overlay opcional (si lo tienes)
      $("#sidebarOverlay").toggleClass("show");

      // Prevenir scroll del body cuando sidebar está abierta
      if ($("#accordionSidebar").hasClass("show")) {
        $("body").css("overflow", "hidden");
      } else {
        $("body").css("overflow", "");
      }
    }
  });

  // ============================================================
  // CERRAR SIDEBAR AL HACER CLICK EN OVERLAY (MÓVIL)
  // ============================================================

  $(document).on('click', '#sidebarOverlay', function() {
    if ($(window).width() <= 900) {
      $("#accordionSidebar").removeClass("show");
      $("#sidebarOverlay").removeClass("show");
      $("body").css("overflow", "");
    }
  });

  // ============================================================
  // CERRAR SIDEBAR AL HACER CLICK EN LINKS (MÓVIL)
  // ============================================================

  $('#accordionSidebar .nav-link').on('click', function() {
    // Solo cerrar en móvil y si NO es un link con collapse
    if ($(window).width() <= 900 &&
        !$(this).attr('data-toggle') &&
        $("#accordionSidebar").hasClass("show")) {
      $("#accordionSidebar").removeClass("show");
      $("#sidebarOverlay").removeClass("show");
      $("body").css("overflow", "");
    }
  });

  // ============================================================
  // RESPONSIVE: AJUSTES AL CAMBIAR TAMAÑO DE VENTANA
  // ============================================================

  $(window).resize(function() {
    var windowWidth = $(window).width();

    // Si cambias a desktop, limpiar clases de móvil
    if (windowWidth > 900) {
      $("#accordionSidebar").removeClass("show");
      $("#sidebarOverlay").removeClass("show");
      $("body").css("overflow", "");
    }

    // Cerrar collapses en móvil
    if (windowWidth <= 900) {
      $('#accordionSidebar .collapse').collapse('hide');
    }

    // Auto-colapsar sidebar en pantallas muy pequeñas
    if (windowWidth < 480 && !$("#accordionSidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $("#accordionSidebar").addClass("toggled");
      $('#accordionSidebar .collapse').collapse('hide');
    }
  });

  // ============================================================
  // PREVENIR SCROLL CUANDO EL MOUSE ESTÁ SOBRE LA SIDEBAR
  // ============================================================

  $('body.fixed-nav #accordionSidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 900) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // ============================================================
  // BOTÓN "SCROLL TO TOP" - APARECE AL HACER SCROLL
  // ============================================================

  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // ============================================================
  // SMOOTH SCROLLING CON JQUERY EASING
  // ============================================================

  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

  // ============================================================
  // INICIALIZACIÓN: AJUSTAR ESTADO INICIAL SEGÚN ANCHO
  // ============================================================

  $(document).ready(function() {
    // Si cargas la página en móvil, asegurar que sidebar esté oculta
    if ($(window).width() <= 900) {
      $("#accordionSidebar").removeClass("show");
      $("body").css("overflow", "");
    }

    // Si cargas en pantalla pequeña, auto-colapsar
    if ($(window).width() < 480) {
      $("body").addClass("sidebar-toggled");
      $("#accordionSidebar").addClass("toggled");
    }
  });

})(jQuery); // End of use strict