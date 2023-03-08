// Get all the accordion buttons
const teamButtons = document.querySelectorAll('.team_name_btn');

// Loop through the buttons and add event listeners
teamButtons.forEach(button => {
  button.addEventListener('click', () => {
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
