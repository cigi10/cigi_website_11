// Function to toggle the mobile menu
function toggleMenu() {
  const navLinks = document.querySelector('.nav-links');
  const hamburger = document.querySelector('.hamburger');
  
  navLinks.classList.toggle('active');
  hamburger.classList.toggle('active');
}

// Function to open the modal and load the image
function openModal(imageSrc) {
  // Set the image source in the modal
  document.getElementById('modalImage').src = imageSrc;

  // Dynamically set the Pinterest button URL
  const pinterestButton = document.getElementById('pinterestButton');
  pinterestButton.href = `https://www.pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.href)}&media=${encodeURIComponent(imageSrc)}&description=${encodeURIComponent('Description of the image')}`;

  // Show the modal with flex to center content
  document.getElementById('commonModal').style.display = 'flex';
}

// Function to close the modal
function closeModal() {
  document.getElementById('commonModal').style.display = 'none';
}

// Function to download the image
function downloadImage() {
  const imageSrc = document.getElementById('modalImage').src;
  const link = document.createElement('a');
  link.href = imageSrc;
  link.download = imageSrc.split('/').pop(); // Extract the filename from the URL
  link.click();
}

// Example of opening the modal (you can hook this up to your gallery items)
document.querySelectorAll('.gallery-item').forEach(item => {
  item.addEventListener('click', function () {
    const imageSrc = this.querySelector('img').src;
    openModal(imageSrc);
  });
});
