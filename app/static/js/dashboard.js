/**
 * TravelGo - Dashboard & Booking Management Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // Tab toggling for dashboard (Upcoming / Past / Cancelled)
  const tabButtons = document.querySelectorAll('.dash-tab-btn');
  const tabPanels = {
    upcoming: document.getElementById('panel-upcoming'),
    past: document.getElementById('panel-past'),
    cancelled: document.getElementById('panel-cancelled')
  };

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.getAttribute('data-tab');

      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      Object.keys(tabPanels).forEach(key => {
        if (tabPanels[key]) {
          tabPanels[key].style.display = key === tabName ? 'block' : 'none';
        }
      });
    });
  });

  // Booking Cancellation Modal
  const cancelModal = document.getElementById('cancelModal');
  const cancelButtons = document.querySelectorAll('.open-cancel-modal');
  const cancelModalClose = document.getElementById('cancelModalClose');
  const cancelModalDismiss = document.getElementById('cancelModalDismiss');
  const modalBookingIdInput = document.getElementById('modalBookingId');
  const modalBookingText = document.getElementById('modalBookingText');

  cancelButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const bookingId = btn.getAttribute('data-id');
      const itemTitle = btn.getAttribute('data-title');
      const amount = btn.getAttribute('data-amount');

      if (modalBookingIdInput) modalBookingIdInput.value = bookingId;
      if (modalBookingText) {
        modalBookingText.innerHTML = `
          Are you sure you want to cancel booking <strong>#${bookingId}</strong> for <em>${itemTitle}</em>?
          <br><br>
          <span style="color: #059669; font-weight: 600;">Full refund of $${amount}</span> will be credited back, and an AWS SNS cancellation email will be dispatched.
        `;
      }

      if (cancelModal) {
        cancelModal.classList.add('active');
      }
    });
  });

  function closeModal() {
    if (cancelModal) cancelModal.classList.remove('active');
  }

  if (cancelModalClose) cancelModalClose.addEventListener('click', closeModal);
  if (cancelModalDismiss) cancelModalDismiss.addEventListener('click', closeModal);

  if (cancelModal) {
    cancelModal.addEventListener('click', (e) => {
      if (e.target === cancelModal) closeModal();
    });
  }
});
