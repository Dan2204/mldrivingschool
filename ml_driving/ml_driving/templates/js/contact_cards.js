const contactDropdowns = document.querySelectorAll('.admin__contact-dropdowns');

// DROPDOWN ITEMS //
contactDropdowns.forEach((item) => {
  item.addEventListener('click', () => {
    const itemBody = item.nextElementSibling;
    const labelArrow = item.firstElementChild.firstElementChild;
    // const itemLabel = item.firstElementChild;
    item.classList.toggle('active');
    if (item.classList.contains('active')) {
      itemBody.style.maxHeight = itemBody.scrollHeight + 'px';
      labelArrow.style.transform = 'rotate(180deg)';
    } else {
      itemBody.style.maxHeight = 0;
      labelArrow.style.transform = 'rotate(0deg)';
    }
  });
});
