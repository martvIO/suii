const inputs = document.querySelectorAll('input');
const button = document.getElementById('submit');
document.addEventListener('DOMContentLoaded',function(){
    button.disabled = true;
});
inputs.forEach(input => {
  input.addEventListener('input', () => {
    const allInputsFilled = Array.from(inputs).every(input => {
      if (input.type === 'submit') {
        return true; // Ignore the submit button itself
      }
      return input.value.trim() !== '';
    });

    button.disabled = !allInputsFilled;
  });
});
window.addEventListener('DOMContentLoaded', function() {
  let errorMessages = document.querySelectorAll('.error-message');
  errorMessages.forEach(errorMessage => {
    if (errorMessage.textContent !== '') {
      errorMessage.style.display = 'block';
    }
  });
});