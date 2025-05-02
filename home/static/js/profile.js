const avatar = document.getElementById('avatar');
const avatarInput = document.getElementById('avatarInput');

// Load saved avatar on page load
window.onload = () => {
  const savedImage = localStorage.getItem('savedAvatar');
  if (savedImage) {
    avatar.src = savedImage;
  }
};

// Upload image preview
avatarInput.addEventListener('change', function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      avatar.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

// Save avatar to localStorage
function saveAvatar() {
  const imgData = avatar.src;
  localStorage.setItem('savedAvatar', imgData);
  alert('Avatar saved successfully!');
}

// Reset avatar
function resetAvatar() {
  avatar.src = 'avatar.png';
  localStorage.removeItem('savedAvatar');
}
