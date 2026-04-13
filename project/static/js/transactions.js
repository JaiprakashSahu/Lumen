/**
 * Center-Focus Scroll Animation
 *
 * Reusable scroll effect for any page with a scrollable list of cards.
 * Detects how far each card is from the scroll container's vertical center
 * and dynamically applies a smooth transform-only motion via inline
 * styles. Uses requestAnimationFrame to avoid layout thrashing.
 *
 * Supports: Transactions page + Receipts page (and any future page).
 */
(function () {
  'use strict';

  /* ── Config ───────────────────────────────────────────────────────── */
  var CFG = {
    scaleXMin:   0.92,
    scaleXMax:   1.01,
    scaleYMin:   0.80,
    scaleYMax:   1.01,
    offsetMax:   28,    // px offset to curve cards away from center
    rotateXMax:  64,    // deg tilt for top/bottom cards
    popZ:        68,    // px: center card pops out toward viewer
    sideZ:      -36,    // px: side cards sink back
    falloff:    320     // distance (px) at which a card is fully "far"
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

  function parseAmount(value) {
    var n = Number(String(value || 0).replace(/[^0-9.-]/g, ''));
    return Number.isFinite(n) ? n : 0;
  }

  function csvEscape(value) {
    var str = value == null ? '' : String(value);
    if (/[",\n]/.test(str)) {
      return '"' + str.replace(/"/g, '""') + '"';
    }
    return str;
  }

  function downloadCsv(filename, headers, rows) {
    var csv = [headers.join(',')]
      .concat(rows.map(function (row) {
        return headers.map(function (h) { return csvEscape(row[h]); }).join(',');
      }))
      .join('\n');

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
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
    if (!container) return null;

    function getCards() {
      return Array.prototype.slice.call(container.querySelectorAll(cardSelector));
    }

    var cards = getCards();
    if (cards.length === 0) return null;

    var ticking = false;

    function applyFocus() {
      cards = getCards();
      if (cards.length === 0) {
        ticking = false;
        return;
      }

      if (container.dataset.view === 'list') {
        for (var i = 0; i < cards.length; i++) {
          cards[i].style.transform = 'none';
          cards[i].style.opacity = '1';
          cards[i].style.filter = 'none';
          cards[i].style.boxShadow = 'none';
          cards[i].style.zIndex = '1';
          cards[i].classList.remove('is-focused');
        }
        ticking = false;
        return;
      }

      var rect    = container.getBoundingClientRect();
      var centerY = rect.top + rect.height * 0.5;
      var closest = null;
      var closestD = Infinity;

      for (var i = 0; i < cards.length; i++) {
        var card       = cards[i];
        var cRect      = card.getBoundingClientRect();
        var cardCenter = cRect.top + cRect.height * 0.5;
        var dist       = Math.abs(cardCenter - centerY);
        var dir        = cardCenter < centerY ? -1 : 1;

        // Normalise: 0 = dead center, 1 = fully far
        var t = clamp(dist / CFG.falloff, 0, 1);
        var ease = Math.pow(t, 0.78);

        var scaleX = lerp(CFG.scaleXMax, CFG.scaleXMin, ease);
        var scaleY = lerp(CFG.scaleYMax, CFG.scaleYMin, ease);
        var offset = dir * lerp(0, CFG.offsetMax, ease);
        var rotateX = dir * lerp(0, CFG.rotateXMax, ease);
        var zDepth = lerp(CFG.popZ, CFG.sideZ, ease);

        card.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,' + zDepth.toFixed(2) + 'px) rotateX(' + rotateX.toFixed(2) + 'deg) scale(' + scaleX.toFixed(4) + ',' + scaleY.toFixed(4) + ')';
        card.style.opacity = '1';
        card.style.filter = 'none';
        card.style.zIndex = String(2000 - Math.round(dist));

        if (dist < closestD) {
          closestD = dist;
          closest  = card;
        }
      }

      // Toggle .is-focused on nearest card
      for (var j = 0; j < cards.length; j++) {
        if (cards[j] === closest) {
          cards[j].classList.add('is-focused');
          cards[j].style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.26)';
        } else {
          cards[j].classList.remove('is-focused');
          cards[j].style.boxShadow = 'none';
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

    return {
      container: container,
      refresh: onScroll,
      getCards: getCards
    };
  }

  function initViewToggle(uiId, blockBtnId, listBtnId, focusEngine) {
    var ui = document.getElementById(uiId);
    var blockBtn = document.getElementById(blockBtnId);
    var listBtn = document.getElementById(listBtnId);
    if (!ui || !blockBtn || !listBtn || !focusEngine) return;

    blockBtn.addEventListener('click', function () {
      ui.classList.remove('is-list');
      blockBtn.classList.add('active');
      listBtn.classList.remove('active');
      focusEngine.container.dataset.view = 'block';
      focusEngine.refresh();
    });

    listBtn.addEventListener('click', function () {
      ui.classList.add('is-list');
      listBtn.classList.add('active');
      blockBtn.classList.remove('active');
      focusEngine.container.dataset.view = 'list';
      focusEngine.refresh();
    });
  }

  function initSortButton(buttonId, focusEngine, cardSelector) {
    var btn = document.getElementById(buttonId);
    if (!btn || !focusEngine) return;

    var asc = false;
    btn.addEventListener('click', function () {
      var container = focusEngine.container;
      var cards = focusEngine.getCards();
      var spacers = container.querySelectorAll('.txn-scroll-spacer, .rcpt-scroll-spacer');
      var bottomSpacer = spacers.length ? spacers[spacers.length - 1] : null;

      cards.sort(function (a, b) {
        var av = parseAmount(a.dataset.amount);
        var bv = parseAmount(b.dataset.amount);
        return asc ? av - bv : bv - av;
      });

      for (var i = 0; i < cards.length; i++) {
        container.insertBefore(cards[i], bottomSpacer);
      }

      asc = !asc;
      btn.textContent = asc ? 'Sort ↑' : 'Sort ↓';
      focusEngine.refresh();
    });
  }

  function initExportButton(buttonId, cardSelector, filename, rowMapper) {
    var btn = document.getElementById(buttonId);
    if (!btn) return;

    btn.addEventListener('click', function () {
      var cards = Array.prototype.slice.call(document.querySelectorAll(cardSelector));
      if (!cards.length) return;

      var rows = cards.map(rowMapper);
      var headers = Object.keys(rows[0] || {});
      if (!headers.length) return;
      downloadCsv(filename, headers, rows);
    });
  }

  /* ── Init ──────────────────────────────────────────────────────────── */
  function init() {
    // Transactions page
    var txnFx = initScrollEffect('txnScrollContainer', '.txn-card');

    // Receipts page
    var rcptFx = initScrollEffect('receiptScrollContainer', '.receipt-card');

    initViewToggle('txnUi', 'txnViewBlock', 'txnViewList', txnFx);
    initViewToggle('rcptUi', 'rcptViewBlock', 'rcptViewList', rcptFx);

    initSortButton('txnSortBtn', txnFx, '.txn-card');
    initSortButton('rcptSortBtn', rcptFx, '.receipt-card');

    initExportButton('txnExportBtn', '.txn-card', 'transactions.csv', function (card) {
      return {
        Name: card.dataset.name || '',
        Date: card.dataset.date || '',
        Amount: card.dataset.amount || '',
        Category: (card.querySelector('.txn-pill') || {}).textContent || ''
      };
    });

    initExportButton('rcptExportBtn', '.receipt-card', 'receipts.csv', function (card) {
      return {
        Vendor: card.dataset.vendor || '',
        Date: card.dataset.date || '',
        Amount: card.dataset.amount || '',
        Type: ((card.querySelector('.receipt-pill') || {}).textContent || '').trim()
      };
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
