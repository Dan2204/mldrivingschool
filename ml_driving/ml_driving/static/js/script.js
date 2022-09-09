const ddCourses = document.getElementById('dd-courses');
const linkCourses = document.getElementById('link-courses');
const ddLearners = document.getElementById('dd-learners');
const linkLearners = document.getElementById('link-learners');
const ddReviews = document.getElementById('dd-reviews');
const linkReviews = document.getElementById('link-reviews');
const toggleBtn = document.getElementById('toggle-btn');
const navLinks = document.getElementById('nav-links');
const accordionItems = document.querySelectorAll('.accordion-item');

// NAVIGATION LINK ITEMS AND DROPDOWN ITEMS
linkCourses.addEventListener('click', () => {
  ddCourses.classList.toggle('show');
  ddLearners.classList.remove('show');
  ddReviews.classList.remove('show');
});

linkLearners.addEventListener('click', () => {
  ddLearners.classList.toggle('show');
  ddCourses.classList.remove('show');
  ddReviews.classList.remove('show');
});

linkReviews.addEventListener('click', () => {
  ddReviews.classList.toggle('show');
  ddLearners.classList.remove('show');
  ddCourses.classList.remove('show');
});

document.addEventListener('click', (e) => {
  if (e.target.closest('a')) return;
  ddLearners.classList.remove('show');
  ddCourses.classList.remove('show');
  ddReviews.classList.remove('show');
});

toggleBtn.addEventListener('click', () => {
  navLinks.classList.toggle('show-menu');
});

// ACCORDION ITEMS

accordionItems.forEach((item) => {
  item.addEventListener('click', () => {
    const itemLabel = item.firstElementChild;
    const labelArrow = itemLabel.firstElementChild.firstElementChild;
    const itemBody = itemLabel.nextElementSibling;
    item.classList.toggle('active');
    if (item.classList.contains('active')) {
      itemBody.style.maxHeight = itemBody.scrollHeight + 'px';
      labelArrow.style.transform = 'rotate(180deg)';
      console.log('Element styles set.');
      accordionItems.forEach((resetItem) => {
        const resetItemLabel = resetItem.firstElementChild;
        if (resetItemLabel !== itemLabel) {
          const arrow = resetItemLabel.firstElementChild.firstElementChild;
          resetItemLabel.nextElementSibling.style.maxHeight = 0;
          arrow.style.transform = 'rotate(0deg)';
          resetItem.classList.remove('active');
        }
      });
    } else {
      itemBody.style.maxHeight = 0;
      labelArrow.style.transform = 'rotate(0deg)';
    }
  });
});
