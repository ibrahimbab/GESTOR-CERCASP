// Example client-side validations
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Example: Validate age >18
            const age = form.querySelector('input[name="age"]');
            if (age && parseInt(age.value) < 18) {
                alert('Edad debe ser mayor a 18');
                e.preventDefault();
            }
        });
    });
});
