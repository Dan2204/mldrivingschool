const ddCourses = document.getElementById('dd-courses');
const linkCourses = document.getElementById('link-courses');
const ddLearners = document.getElementById('dd-learners');
const linkLearners = document.getElementById('link-learners');
const ddReviews = document.getElementById('dd-reviews');
const linkReviews = document.getElementById('link-reviews');
const toggleBtn = document.getElementById('toggle-btn');
const navLinks = document.getElementById('nav-links');

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
