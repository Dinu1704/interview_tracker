document.addEventListener('DOMContentLoaded', function() {
    // Select all forms that need validation
    const forms = document.querySelectorAll('form[novalidate]');

    // Function to handle validation for a single input
    const validateInput = (input) => {
        if (input.checkValidity()) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            // Find the corresponding invalid-feedback div and update its message
            const feedback = input.parentElement.querySelector('.invalid-feedback');
            if (feedback) {
                if (input.validity.valueMissing) {
                    feedback.textContent = input.parentElement.querySelector('label').textContent.replace('*', '') + ' is required.';
                } else if (input.validity.patternMismatch) {
                    feedback.textContent = 'Please enter a valid 10-digit contact number.';
                }
            }
            return false;
        }
    };

    forms.forEach(form => {
        // Validate on submit
        form.addEventListener('submit', function(event) {
            let isFormValid = true;
            const inputsToValidate = form.querySelectorAll('input[required], input[pattern]');

            inputsToValidate.forEach(input => {
                if (!validateInput(input)) {
                    isFormValid = false;
                }
            });

            if (!isFormValid) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        // Validate on input/change for immediate feedback
        const inputsToValidate = form.querySelectorAll('input[required], input[pattern]');
        inputsToValidate.forEach(input => {
            input.addEventListener('input', () => {
                // Only show validation feedback after the user has started typing
                // and the form has been submitted once, or on blur
                if (form.classList.contains('was-validated')) {
                    validateInput(input);
                }
            });
            input.addEventListener('blur', () => {
                // Validate when the user leaves the field
                validateInput(input);
                form.classList.add('was-validated'); // Start showing validation feedback
            });
        });
    });
});
