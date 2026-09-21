/**
 * MOD-CAROUSEL — Swiper + estados + mosaico (TASK-008 / 008b / 016 / 017)
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
    if (state === "empty") {
      return;
    }

    if (slide.getAttribute("data-layout") === "mosaic") {
      wireMosaicSlide(slide);
      return;
    }

    var iframe = slide.querySelector(".dsn-embed-iframe");
    var loading = slide.querySelector(".dsn-state--loading");
    var error = slide.querySelector(".dsn-state--error");

    if (!iframe) {
      setState(slide, "empty");
      return;
    }

    wireIframe(slide, iframe, loading, error);
  }

  function wireMosaicSlide(slide) {
    var iframes = slide.querySelectorAll(".dsn-embed-iframe");
    if (!iframes.length) {
      setState(slide, "empty");
      return;
    }

    setState(slide, "loading");
    var pending = iframes.length;
    var failed = 0;

    function settleOne(ok) {
      if (!ok) failed += 1;
      pending -= 1;
      if (pending > 0) return;
      setState(slide, failed === iframes.length ? "error" : "ready");
      slide.querySelectorAll(".dsn-state--loading").forEach(function (el) {
        el.hidden = true;
      });
      if (failed === iframes.length) {
        slide.querySelectorAll(".dsn-state--error").forEach(function (el) {
          el.hidden = false;
        });
      }
    }

    iframes.forEach(function (iframe) {
      var wrap = iframe.closest(".embed-wrapper") || iframe.parentElement;
      var loading = wrap && wrap.querySelector(".dsn-state--loading");
      var error = wrap && wrap.querySelector(".dsn-state--error");
      if (loading) loading.hidden = false;

      var done = false;
      function ok() {
        if (done) return;
        done = true;
        if (loading) loading.hidden = true;
        settleOne(true);
      }
      function bad() {
        if (done) return;
        done = true;
        if (loading) loading.hidden = true;
        if (error) error.hidden = false;
        settleOne(false);
      }

      iframe.addEventListener("load", ok);
      iframe.addEventListener("error", bad);
      setTimeout(ok, 12000);
    });

    // KPIs nativos já no DOM ⇒ shell útil imediato
    if (slide.querySelector(".dsn-kpi")) {
      slide.setAttribute("data-kpis-ready", "1");
    }

    if (/dsn_force_error=1/.test(window.location.search)) {
      setState(slide, "error");
    }
  }

  function wireIframe(slide, iframe, loading, error) {
    setState(slide, "loading");
    if (loading) loading.hidden = false;

    var settled = false;

    function markReady() {
      if (settled) return;
      settled = true;
      setState(slide, "ready");
      if (loading) loading.hidden = true;
      if (error) error.hidden = true;
    }

    function markError() {
      if (settled) return;
      settled = true;
      setState(slide, "error");
      if (loading) loading.hidden = true;
      if (error) error.hidden = false;
      iframe.style.display = "none";
    }

    iframe.addEventListener("load", markReady);
    iframe.addEventListener("error", markError);

    try {
      if (iframe.contentDocument && iframe.contentDocument.readyState === "complete") {
        markReady();
      }
    } catch (e) {
      /* cross-origin */
    }
    setTimeout(markReady, 12000);

    if (/dsn_force_error=1/.test(window.location.search)) {
      markError();
    }
  }

  function setState(slide, state) {
    slide.setAttribute("data-state", state);
  }

  document.addEventListener("DOMContentLoaded", function () {
    /* BUG-003: chrome do tema WP fica display:none no dashboard — aria-hidden evita axe serious em <ul> aninhados */
    if (document.body.classList.contains("dsn-no-scroll")) {
      document
        .querySelectorAll(
          ".wp-site-blocks > header, .wp-site-blocks > footer, header.wp-block-template-part, footer.wp-block-template-part, .entry-header, #wpadminbar"
        )
        .forEach(function (el) {
          el.setAttribute("aria-hidden", "true");
          el.setAttribute("inert", "");
        });
    }
    document.querySelectorAll(".dsn-dashboard").forEach(initDashboard);
  });
})();
