function setupProfileActions(modal) {
    const buttons = modal.querySelectorAll('.buttons');
    const buttonText = modal.querySelector('.autorizationTitle');
    const registrationText = modal.querySelector('.registrationTitle');

    function redirectToAuth() {
        window.location.href = "{% url 'autorization' %}";
    }

    buttons.forEach(button => {
        button.addEventListener('click', redirectToAuth);
    });

    if (buttonText) {
        buttonText.addEventListener('click', redirectToAuth);
    }

    if (registrationText) {
        registrationText.addEventListener('click', function() {
            window.location.href = "{% url 'registration' %}";
        });
    }
}