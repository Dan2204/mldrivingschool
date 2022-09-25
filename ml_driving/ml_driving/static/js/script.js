// NAVIGATION LINK ITEMS, DROPDOWN ITEMS AND ACCORDION ITEMS //
const ddCourses = document.getElementById('dd-courses');
const linkCourses = document.getElementById('link-courses');
const ddLearners = document.getElementById('dd-learners');
const linkLearners = document.getElementById('link-learners');
const ddReviews = document.getElementById('dd-reviews');
const linkReviews = document.getElementById('link-reviews');
const toggleBtn = document.getElementById('toggle-btn');
const navLinks = document.getElementById('nav-links');
const accordionItems = document.querySelectorAll('.accordion-item');

// NAVIGATION LINK ITEMS AND DROPDOWN ITEMS //
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

// ACCORDION ITEMS //
accordionItems.forEach((item) => {
  item.addEventListener('click', () => {
    const itemLabel = item.firstElementChild;
    const labelArrow = itemLabel.firstElementChild.firstElementChild;
    const itemBody = itemLabel.nextElementSibling;
    item.classList.toggle('active');
    if (item.classList.contains('active')) {
      itemBody.style.maxHeight = itemBody.scrollHeight + 'px';
      labelArrow.style.transform = 'rotate(180deg)';
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

// IMAGE UPLOAD AND PASSWORD CHANGE //
let input_pic = document.getElementById('img-upload');
let img_txt = document.getElementById('img-txt');
let img_txt_file = document.getElementById('img-filename');
let edit_img_txt = document.getElementById('edit-img-txt');
const imgForm = document.querySelector('.image-form');
const imgFormBtn = document.getElementById('img-btn');
const imgFormHead = document.getElementById('img-form-head');
const imgModal = document.querySelector('.image-form-container');
const noteModal = document.querySelector('.note-form-container');
const passwordModal = document.querySelector('.password-form-container');
const openImgModal = document.getElementById('add-img-modal');
const openNoteModal = document.querySelectorAll('.add-note-modal');
const contact_input = document.querySelector('.note-contact_id');
const openPasswordModal = document.getElementById('change-pw-modal');
const closeModal = document.querySelectorAll('.close');
const uploadErrors = document.getElementById('img-ul-err');
const adminNavItems = document.querySelectorAll('.admin-item');

window.addEventListener('load', () => {
  if (modals) {
    if (modals.upload === 'open' && imgModal) {
      toggleModalElement(imgModal, 'upload', 'open');
      adminNavItems.forEach((item) => {
        if (item.classList.contains('link_img-ul')) {
          item.classList.add('sub-active');
        }
      });
    } else {
      if (imgModal) {
        toggleModalElement(imgModal, 'upload', 'closed');
      }
    }
    if (modals.password === 'open' && passwordModal) {
      toggleModalElement(passwordModal, 'password', 'open');
      adminNavItems.forEach((item) => {
        if (item.classList.contains('link_password')) {
          item.classList.add('sub-active');
        }
      });
    } else {
      if (passwordModal) {
        toggleModalElement(passwordModal, 'password', 'closed');
      }
    }
    // if (modals.note === 'open' && noteModal) {
    //   toggleModalElement(noteModal, 'note', 'open');
    //   console.log(openNoteModal);
    //   contact_input.value = note.dataset.contact;
    // } else {
    //   if (noteModal) {
    //     toggleModalElement(noteModal, 'note', 'closed');
    //   }
    // }
  }
});

document.addEventListener('click', (e) => {
  if (
    (!e.target.closest('.image-form') &&
      e.target.closest('.image-form-container.show')) ||
    (!e.target.closest('.password-form') &&
      e.target.closest('.password-form-container.show')) ||
    (!e.target.closest('.note-form') && e.target.closest('.note-form-container.show'))
  ) {
    toggleModalElement(imgModal, 'upload', 'closed');
    toggleModalElement(noteModal, 'note', 'closed');
    toggleModalElement(passwordModal, 'password', 'closed');
    adminNavItems.forEach((item) => {
      item.classList.remove('sub-active');
    });
  }
});

if (openImgModal) {
  openImgModal.addEventListener('click', (e) => {
    adminNavItems.forEach((item) => {
      if (item.classList.contains('link_img-ul')) {
        item.classList.add('sub-active');
      }
    });
    toggleModalElement(imgModal, 'upload', 'open');
  });
}

if (openNoteModal) {
  openNoteModal.forEach((note) => {
    note.addEventListener('click', (e) => {
      toggleModalElement(noteModal, 'note', 'open');
      console.log(openNoteModal);
      console.log(note);
      console.log(note.dataset.contact);
      contact_input.value = note.dataset.contact;
    });
  });
}

if (openPasswordModal) {
  openPasswordModal.addEventListener('click', (e) => {
    adminNavItems.forEach((item) => {
      if (item.classList.contains('link_password')) {
        item.classList.add('sub-active');
      }
    });
    toggleModalElement(passwordModal, 'password', 'open');
  });
}

if (closeModal) {
  closeModal.forEach((x) => {
    x.addEventListener('click', () => {
      adminNavItems.forEach((item) => {
        item.classList.remove('sub-active');
      });
      console.log('Calling close imgModal');
      toggleModalElement(imgModal, 'upload', 'closed');
      console.log('Calling close passwordModal');
      toggleModalElement(passwordModal, 'password', 'closed');
      toggleModalElement(noteModal, 'note', 'closed');
      // edit_img_txt.classList.remove('form-edit');
    });
  });
}

const toggleModalElement = (element, storageItem, mode) => {
  if (element) {
    if (mode === 'open') {
      element.classList.add('show');
    } else if (mode === 'closed') {
      element.classList.remove('show');
    } else {
      return;
    }
    sessionStorage.setItem(storageItem, mode);
    modals[storageItem] = mode;
  }
};

if (input_pic) {
  input_pic.addEventListener('change', (e) => {
    if (input_pic.value) {
      style_image = document.getElementById('on-post-image');
      style_image.firstElementChild.style.color = '#67BD3D';
      let pic_val = input_pic.value.split('\\');
      pic_val = pic_val[pic_val.length - 1];
      if (pic_val.length > 19) {
        pic_file_type = pic_val.slice(pic_val.length - 4);
        pic_val = pic_val.slice(0, 14) + '.. ' + pic_file_type;
      }
      img_txt.childNodes[0].nodeValue = 'Image Added:';
      img_txt_file.textContent = '"' + pic_val + '"';
      if (edit_img_txt) {
        edit_img_txt.childNodes[0].nodeValue = '(Replacing image)';
      }
      if (uploadErrors) {
        uploadErrors.textContent = '';
      }
    } else {
      style_image = document.getElementById('on-post-image');
      style_image.firstElementChild.style.color = '#fff';
      img_txt.childNodes[0].nodeValue = 'Add Image: ';
      img_txt_file.textContent = '';
      if (edit_img_txt) {
        edit_img_txt.childNodes[0].nodeValue = '(Leave to keep current image)';
      }
      if (uploadErrors) {
        uploadErrors.textContent = 'This field is required.';
      }
    }
  });
}

// HIDE ERROR MESSAGES WHEN USER TYPES IN FIELD //
const errorMessage = document.getElementsByClassName('comment-error');
const inputBox = document.getElementsByClassName('logging-input');

if (errorMessage) {
  for (let i = 0; i < inputBox.length; i++) {
    inputBox[i].addEventListener('keypress', hideErrors);
  }

  function hideErrors() {
    for (let i = 0; i < errorMessage.length; i++) {
      errorMessage[i].style.display = 'none';
    }
  }
}
