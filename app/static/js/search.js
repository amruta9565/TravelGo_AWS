/**
 * TravelGo - Multi-Modal Search Widget Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const forms = document.querySelectorAll('.search-form');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetService = btn.getAttribute('data-tab');

      // Update tabs
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Show relevant form
      forms.forEach(form => {
        if (form.getAttribute('data-service') === targetService) {
          form.classList.add('active');
        } else {
          form.classList.remove('active');
        }
      });
    });
  });

  // Hotel Category Filter Pills (All, Budget, Luxury)
  const hotelPills = document.querySelectorAll('.filter-pill');
  const hotelCategoryInput = document.getElementById('hotelCategoryInput');

  hotelPills.forEach(pill => {
    pill.addEventListener('click', () => {
      hotelPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const category = pill.getAttribute('data-category');
      if (hotelCategoryInput) {
        hotelCategoryInput.value = category;
      }
    });
  });
});
