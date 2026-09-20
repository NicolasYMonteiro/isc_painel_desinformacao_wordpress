/**
 * MOD-CAROUSEL — Swiper init + estados loading/error/empty (TASK-008/016/017)
 */
(function () {
  function initDashboard(root) {
    var initial = Math.max(0, (parseInt(root.getAttribute("data-initial-slide"), 10) || 1) - 1);
    var speed = (window.dsnDash && window.dsnDash.transitionMs) || 280;

    var swiper = new Swiper(root.querySelector(".dsn-swiper"), {
      slidesPerView: 1,
      speed: speed,
      keyboard: { enabled: true },
      navigation: {
        nextEl: root.querySelector(".swiper-button-next"),
        prevEl: root.querySelector(".swiper-button-prev"),
      },
      pagination: {
        el: root.querySelector(".swiper-pagination"),
        clickable: true,
      },
      initialSlide: initial,
      watchOverflow: true,
    });

    root.querySelectorAll(".dsn-slide").forEach(function (slide) {
      wireSlide(slide);
    });

    return swiper;
  }

  function wireSlide(slide) {
    var state = slide.getAttribute("data-state") || "loading";
    var iframe = slide.querySelector(".dsn-embed-iframe");
    var loading = slide.querySelector(".dsn-state--loading");
    var error = slide.querySelector(".dsn-state--error");

    if (state === "empty") {
      return;
    }

    if (!iframe) {
      setState(slide, "empty");
      return;
    }

    setState(slide, "loading");
    if (loading) loading.hidden = false;

    var settled = false;
    var timer = setTimeout(function () {
      if (!settled) {
        // timeout: ainda pode estar ok, mas marcamos ready se load já veio
      }
    }, 5000);

    iframe.addEventListener("load", function () {
      settled = true;
      clearTimeout(timer);
      setState(slide, "ready");
      if (loading) loading.hidden = true;
      if (error) error.hidden = true;
    });

    iframe.addEventListener("error", function () {
      settled = true;
      clearTimeout(timer);
      setState(slide, "error");
      if (loading) loading.hidden = true;
      if (error) error.hidden = false;
      iframe.style.display = "none";
    });

    // Detecção limitada de framing: se após 8s iframe continuar "opaco"/vazio
    // o operador usa ?dsn_force_error=1 para testar UC-06
    if (/dsn_force_error=1/.test(window.location.search)) {
      setState(slide, "error");
      if (loading) loading.hidden = true;
      if (error) error.hidden = false;
      iframe.style.display = "none";
    }
  }

  function setState(slide, state) {
    slide.setAttribute("data-state", state);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".dsn-dashboard").forEach(initDashboard);
  });
})();
