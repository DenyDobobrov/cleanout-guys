/**
 * CLEANOUT GUYS — MAIN JAVASCRIPT
 * cleanout-guys.com
 * Handles: Nav, FAQ accordion, Stats counter, Back to top, Form validation
 */

'use strict';

// ─────────────────────────────────────────────
// DOM READY
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  setYear();
  initMobileNav();
  initFAQAccordion();
  initStatsCounter();
  initBackToTop();
  initStickyHeader();
  initFormValidation();
  trackPhoneClicks();
});

// ─────────────────────────────────────────────
// SET CURRENT YEAR
// ─────────────────────────────────────────────
function setYear() {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
}

// ─────────────────────────────────────────────
// MOBILE NAVIGATION
// ─────────────────────────────────────────────
function initMobileNav() {
  const toggle = document.getElementById('menu-toggle');
  const nav    = document.getElementById('main-nav');
  const close  = document.getElementById('nav-close');

  if (!toggle || !nav) return;

  function openNav() {
    nav.classList.add('mobile-open');
    toggle.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeNav() {
    nav.classList.remove('mobile-open');
    toggle.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  toggle.addEventListener('click', function () {
    nav.classList.contains('mobile-open') ? closeNav() : openNav();
  });

  if (close) close.addEventListener('click', closeNav);

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('mobile-open') &&
        !nav.contains(e.target) &&
        !toggle.contains(e.target)) {
      closeNav();
    }
  });

  // Close on escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeNav();
  });
}

// ─────────────────────────────────────────────
// FAQ ACCORDION
// ─────────────────────────────────────────────
function initFAQAccordion() {
  const items = document.querySelectorAll('.faq-item');

  items.forEach(function (item) {
    const question = item.querySelector('.faq-question');
    const answer   = item.querySelector('.faq-answer');

    if (!question || !answer) return;

    function toggleItem() {
      const isOpen = item.classList.contains('open');

      // Close all others
      items.forEach(function (other) {
        if (other !== item) {
          other.classList.remove('open');
          const otherAnswer = other.querySelector('.faq-answer');
          const otherQ = other.querySelector('.faq-question');
          if (otherAnswer) otherAnswer.style.maxHeight = null;
          if (otherQ) otherQ.setAttribute('aria-expanded', 'false');
        }
      });

      // Toggle current
      if (isOpen) {
        item.classList.remove('open');
        answer.style.maxHeight = null;
        question.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
        question.setAttribute('aria-expanded', 'true');
      }
    }

    question.addEventListener('click', toggleItem);
    question.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleItem();
      }
    });
  });
}

// ─────────────────────────────────────────────
// ANIMATED STATS COUNTER
// ─────────────────────────────────────────────
function initStatsCounter() {
  const statNums = document.querySelectorAll('[data-target]');
  if (!statNums.length) return;

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateStat(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statNums.forEach(function (el) { observer.observe(el); });
}

function animateStat(el) {
  const target   = parseFloat(el.getAttribute('data-target'));
  const suffix   = el.querySelector('.stat-suffix') ? el.querySelector('.stat-suffix').outerHTML : '';
  const isDecimal = target % 1 !== 0;
  const duration = 2000;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed  = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current  = eased * target;

    el.innerHTML = (isDecimal ? current.toFixed(1) : Math.floor(current)) + suffix;

    if (progress < 1) requestAnimationFrame(update);
    else el.innerHTML = target + suffix;
  }

  requestAnimationFrame(update);
}

// ─────────────────────────────────────────────
// BACK TO TOP BUTTON
// ─────────────────────────────────────────────
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ─────────────────────────────────────────────
// STICKY HEADER SHADOW ON SCROLL
// ─────────────────────────────────────────────
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', function () {
    header.style.boxShadow = window.scrollY > 10
      ? '0 4px 24px rgba(0,0,0,.18)'
      : '0 4px 16px rgba(0,0,0,.14)';
  }, { passive: true });
}

// ─────────────────────────────────────────────
// FORM VALIDATION (Quote / Contact form)
// ─────────────────────────────────────────────
function initFormValidation() {
  const form = document.getElementById('quote-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (validateForm(form)) {
      submitForm(form);
    }
  });

  // Real-time validation
  const inputs = form.querySelectorAll('.form-input, .form-select, .form-textarea');
  inputs.forEach(function (input) {
    input.addEventListener('blur', function () { validateField(input); });
    input.addEventListener('input', function () {
      if (input.classList.contains('error')) validateField(input);
    });
  });
}

function validateField(field) {
  const errorEl = field.parentElement.querySelector('.form-error') ||
                  field.closest('.form-group')?.querySelector('.form-error');
  const value = field.value.trim();
  let error = '';

  if (field.hasAttribute('required') && !value) {
    error = 'This field is required.';
  } else if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    error = 'Please enter a valid email address.';
  } else if (field.type === 'tel' && value && !/^\+?[\d\s\-().]{7,}$/.test(value)) {
    error = 'Please enter a valid phone number.';
  }

  if (error) {
    field.classList.add('error');
    if (errorEl) { errorEl.textContent = error; errorEl.classList.add('visible'); }
    return false;
  } else {
    field.classList.remove('error');
    if (errorEl) { errorEl.textContent = ''; errorEl.classList.remove('visible'); }
    return true;
  }
}

function validateForm(form) {
  const fields = form.querySelectorAll('.form-input[required], .form-select[required], .form-textarea[required]');
  let valid = true;
  fields.forEach(function (f) { if (!validateField(f)) valid = false; });
  return valid;
}

function submitForm(form) {
  const btn = form.querySelector('[type="submit"]');
  const successMsg = document.getElementById('form-success');

  // Disable button + show loading
  if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }

  // Collect form data
  const data = new FormData(form);
  const payload = {};
  data.forEach(function (v, k) { payload[k] = v; });

  // In production, replace with real form endpoint (Formspree, Netlify Forms, etc.)
  // fetch('https://formspree.io/f/YOUR_ID', { method: 'POST', body: data })

  // Simulated success (replace with real API call)
  setTimeout(function () {
    form.style.display = 'none';
    if (successMsg) successMsg.classList.add('visible');

    // Push to Google Analytics / GTM
    if (typeof gtag !== 'undefined') {
      gtag('event', 'form_submit', { event_category: 'lead', event_label: 'quote_form' });
    }
    if (typeof dataLayer !== 'undefined') {
      dataLayer.push({ event: 'quote_form_submit' });
    }
  }, 1200);
}

// ─────────────────────────────────────────────
// PHONE CLICK TRACKING
// ─────────────────────────────────────────────
function trackPhoneClicks() {
  document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'phone_call', { event_category: 'lead', event_label: 'phone_click' });
      }
      if (typeof dataLayer !== 'undefined') {
        dataLayer.push({ event: 'phone_click' });
      }
    });
  });
}

// ─────────────────────────────────────────────
// SMOOTH SCROLL FOR ANCHOR LINKS
// ─────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const headerOffset = document.querySelector('.site-header')?.offsetHeight || 80;
      const top = target.getBoundingClientRect().top + window.scrollY - headerOffset - 20;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ─────────────────────────────────────────────
// LAZY LOAD IMAGES (IntersectionObserver)
// ─────────────────────────────────────────────
if ('IntersectionObserver' in window) {
  const lazyImages = document.querySelectorAll('img[data-src]');
  const imgObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        if (img.dataset.srcset) img.srcset = img.dataset.srcset;
        img.classList.add('loaded');
        imgObserver.unobserve(img);
      }
    });
  }, { rootMargin: '200px' });

  lazyImages.forEach(function (img) { imgObserver.observe(img); });
}
