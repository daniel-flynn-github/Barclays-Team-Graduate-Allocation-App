// Get all the accordion buttons
const teamButtons = document.querySelectorAll('.team_name_btn');

// Loop through the buttons and add event listeners
teamButtons.forEach(button => {
  button.addEventListener('click', () => {
    // Ensure all icons for all other teams are UP
    teamButtons.forEach(btn => {
      if (btn !== button) {
        const icon_btn = btn.querySelector('.bi');
        icon_btn.classList.add('bi-chevron-down');
        icon_btn.classList.remove('bi-chevron-up');
      }
    });

    // Get the icon element
    const icon = button.querySelector('.bi');
    // Toggle the icon class based on whether the accordion is expanded or collapsed
    if (button.getAttribute('aria-expanded') === 'true') {
      icon.classList.add('bi-chevron-down');
      icon.classList.remove('bi-chevron-up');
    } else {
      icon.classList.add('bi-chevron-up');
      icon.classList.remove('bi-chevron-down');
    }
  });
});
