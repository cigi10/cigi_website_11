function toggleMenu() {
  const navLinks = document.querySelector('.nav-links');
  const hamburger = document.querySelector('.hamburger');
  
  navLinks.classList.toggle('active');
  hamburger.classList.toggle('active');
}

// Function to open the modal and load the image
function openModal(imageSrc) {
  document.getElementById('modalImage').src = imageSrc;
  document.getElementById('commonModal').style.display = 'flex';  // Use flex to center content
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

