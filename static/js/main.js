// Custom JavaScript for Zomato Clone

// Add confirmation for delete actions
document.addEventListener('DOMContentLoaded', function() {
    // Add confirmation for delete buttons
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add loading state to submit buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        });
    });
    
    // Add search functionality
    const searchForm = document.querySelector('form[method="get"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('keyup', function(e) {
                if (e.key === 'Enter') {
                    searchForm.submit();
                }
            });
        }
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add toast notifications for messages
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        // Auto-hide success messages after 5 seconds
        if (message.classList.contains('alert-success')) {
            setTimeout(() => {
                message.style.transition = 'opacity 0.5s';
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000);
        }
    });
    
    // Add rating stars display
    const ratingElements = document.querySelectorAll('[data-rating]');
    ratingElements.forEach(element => {
        const rating = parseFloat(element.getAttribute('data-rating'));
        const maxRating = parseInt(element.getAttribute('data-max-rating') || '5');
        
        let starsHTML = '';
        for (let i = 1; i <= maxRating; i++) {
            if (i <= rating) {
                starsHTML += '<span class="text-warning">★</span>';
            } else if (i - 0.5 <= rating) {
                starsHTML += '<span class="text-warning">☆</span>';
            } else {
                starsHTML += '<span class="text-muted">☆</span>';
            }
        }
        
        element.innerHTML = starsHTML;
    });
    
    // Add image preview for file inputs
    const fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewId = this.getAttribute('data-preview');
            const preview = document.getElementById(previewId);
            
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});