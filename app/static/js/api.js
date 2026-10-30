/**
 * TravelGo API Helper
 * Handles CSRF tokens and JSON requests cleanly.
 */

const TravelGoAPI = {
  getCsrfToken: function() {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) return metaTag.getAttribute('content');
    const input = document.querySelector('input[name="csrf_token"]');
    return input ? input.value : '';
  },

  fetchJSON: async function(url, options = {}) {
    const headers = options.headers || {};
    const csrfToken = this.getCsrfToken();
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }

    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }

    options.headers = headers;
    const response = await fetch(url, options);
    const data = await response.json();
    return { ok: response.ok, status: response.status, data };
  }
};
