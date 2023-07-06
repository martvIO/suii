const addVisaForm = document.getElementById("addVisaForm");
const moneyForm = document.getElementById("moneyForm");
const SendMoney = document.getElementById("SendMoney");
const forms = [addVisaForm, moneyForm, SendMoney]
forms.forEach((form) => {
    const inputs = form.querySelectorAll("input:not([type='submit'])");
    inputs.forEach((input) => {
        input.addEventListener("input", () => {
            const allFilled = Array.from(inputs).every((input) => input.value.length !== 0);
            form.querySelector("input[type='submit']").style.display = allFilled ? "block" : "none";
        });
    });
});
document.addEventListener('DOMContentLoaded', (e) => {
    const errorMessage = document.querySelectorAll('.error-message');
    errorMessage.forEach((Message) => {
        if (Message.value !== '') {
            Message.style.display = 'block';
        }
    });
});