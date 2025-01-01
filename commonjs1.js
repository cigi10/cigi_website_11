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
  const modalImage = document.getElementById('modalImage');
  modalImage.src = imageSrc;
  
  // Extract image name from src, replace hyphens with spaces, and set as title
  const imageName = imageSrc.split('/').pop().split('.')[0].replace(/-/g, ' ');
  document.getElementById('modalTitle').textContent = imageName;
  
  // Get alt text from the clicked image and set as description
  const clickedImage = document.querySelector(`img[src="${imageSrc}"]`);
  const altText = clickedImage ? clickedImage.alt : '';
  document.getElementById('modalDescription').textContent = altText;
  
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

// Update event listeners to handle both gallery item and image clicks
document.querySelectorAll('.gallery-item img').forEach(img => {
  img.addEventListener('click', function(e) {
    e.stopPropagation(); // Prevent event bubbling
    openModal(this.src);
  });
});
