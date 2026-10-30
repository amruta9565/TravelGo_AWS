/**
 * TravelGo - Dynamic Bus Seat Selector
 */

document.addEventListener('DOMContentLoaded', () => {
  const seatButtons = document.querySelectorAll('.seat-btn:not(.booked)');
  const selectedSeatsDisplay = document.getElementById('selectedSeatsDisplay');
  const selectedCountDisplay = document.getElementById('selectedCountDisplay');
  const totalPriceDisplay = document.getElementById('totalPriceDisplay');
  const hiddenSeatsInput = document.getElementById('hiddenSeatsInput');
  const proceedBtn = document.getElementById('proceedToCheckoutBtn');

  const pricePerSeat = parseFloat(document.getElementById('pricePerSeatData')?.value || 0);
  const maxSeats = 6;
  const selectedSeats = new Set();

  seatButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const seatNumber = btn.getAttribute('data-seat');

      if (selectedSeats.has(seatNumber)) {
        selectedSeats.delete(seatNumber);
        btn.classList.remove('selected');
      } else {
        if (selectedSeats.size >= maxSeats) {
          if (typeof showToast === 'function') {
            showToast(`You can select a maximum of ${maxSeats} seats per booking.`, 'warning');
          } else {
            alert(`Maximum ${maxSeats} seats allowed.`);
          }
          return;
        }
        selectedSeats.add(seatNumber);
        btn.classList.add('selected');
      }

      updateSummary();
    });
  });

  function updateSummary() {
    const seatsArray = Array.from(selectedSeats).sort();
    const count = seatsArray.length;
    const total = (count * pricePerSeat).toFixed(2);

    if (selectedSeatsDisplay) {
      selectedSeatsDisplay.textContent = count > 0 ? seatsArray.join(', ') : 'None selected';
    }

    if (selectedCountDisplay) {
      selectedCountDisplay.textContent = count;
    }

    if (totalPriceDisplay) {
      totalPriceDisplay.textContent = `$${total}`;
    }

    if (hiddenSeatsInput) {
      hiddenSeatsInput.value = seatsArray.join(',');
    }

    if (proceedBtn) {
      proceedBtn.disabled = count === 0;
      proceedBtn.style.opacity = count === 0 ? '0.5' : '1';
      proceedBtn.style.cursor = count === 0 ? 'not-allowed' : 'pointer';
    }
  }

  // Initial update
  updateSummary();
});
