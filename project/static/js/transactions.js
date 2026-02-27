/**
 * Center-Focus Scroll Animation
 *
 * Reusable scroll effect for any page with a scrollable list of cards.
 * Detects how far each card is from the scroll container's vertical center
 * and dynamically applies scale, opacity, rotateX, and blur via inline
 * transforms.  Uses requestAnimationFrame to avoid layout thrashing.
 *
 * Supports: Transactions page + Receipts page (and any future page).
 */
(function () {
  'use strict';

  /* ── Config ───────────────────────────────────────────────────────── */
  var CFG = {
    scaleMin:   0.85,
    scaleMax:   1.0,
    opacityMin: 0.4,
    opacityMax: 1.0,
    rotateMax:  4,      // degrees
    blurMax:    2,      // px
    falloff:    360     // distance (px) at which a card is fully "far"
  };

  /* ── Month selector (Transactions page only) ──────────────────────── */
  var MONTHS = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
  ];
  var currentDate = new Date();

  window.changeMonth = function (dir) {
    currentDate.setMonth(currentDate.getMonth() + dir);
    var label = document.getElementById('monthLabel');
    if (label) {
      label.textContent = MONTHS[currentDate.getMonth()] + ' ' + currentDate.getFullYear();
    }
  };

  /* ── Helpers ──────────────────────────────────────────────────────── */
  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  /* ── Reusable scroll-focus engine ─────────────────────────────────── */

  /**
   * initScrollEffect(containerId, cardSelector)
   *
   * @param {string} containerId   – id of the scrollable container element
   * @param {string} cardSelector  – CSS selector for the cards inside it
   */
  function initScrollEffect(containerId, cardSelector) {
    var container = document.getElementById(containerId);
    if (!container) return;

    var cards = Array.prototype.slice.call(
      container.querySelectorAll(cardSelector)
    );
    if (cards.length === 0) return;

    var ticking = false;

    function applyFocus() {
      var rect    = container.getBoundingClientRect();
      var centerY = rect.top + rect.height * 0.5;
      var closest = null;
      var closestD = Infinity;

      for (var i = 0; i < cards.length; i++) {
        var card       = cards[i];
        var cRect      = card.getBoundingClientRect();
        var cardCenter = cRect.top + cRect.height * 0.5;
        var dist       = Math.abs(cardCenter - centerY);

        // Normalise: 0 = dead center, 1 = fully far
        var t = clamp(dist / CFG.falloff, 0, 1);

        var scale   = lerp(CFG.scaleMax,  CFG.scaleMin,  t);
        var opacity = lerp(CFG.opacityMax, CFG.opacityMin, t);
        var rotate  = lerp(0, CFG.rotateMax, t);
        var blur    = lerp(0, CFG.blurMax,   t);

        // Cards above center tilt downward, below tilt upward
        if (cardCenter < centerY) rotate = -rotate;

        card.style.transform = 'scale(' + scale.toFixed(4) + ') perspective(800px) rotateX(' + rotate.toFixed(2) + 'deg)';
        card.style.opacity   = opacity.toFixed(3);
        card.style.filter    = blur > 0.05 ? 'blur(' + blur.toFixed(2) + 'px)' : 'none';

        if (dist < closestD) {
          closestD = dist;
          closest  = card;
        }
      }

      // Toggle .is-focused on nearest card
      for (var j = 0; j < cards.length; j++) {
        if (cards[j] === closest) {
          cards[j].classList.add('is-focused');
        } else {
          cards[j].classList.remove('is-focused');
        }
      }

      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(applyFocus);
      }
    }

    container.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });

    // Initial pass
    requestAnimationFrame(applyFocus);
  }

  /* ── Init ──────────────────────────────────────────────────────────── */
  function init() {
    // Transactions page
    initScrollEffect('txnScrollContainer', '.txn-card');

    // Receipts page
    initScrollEffect('receiptScrollContainer', '.receipt-card');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
