document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generate-password');
    const password1Input = document.getElementById('id_password1');
    const password2Input = document.getElementById('id_password2');

    generateButton.addEventListener('click', function() {
        const password = generatePassword(12);
        password1Input.value = password;
        password2Input.value = password;
    });

    function generatePassword(length) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
        let password = "";
        for (let i = 0; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        return password;
    }
});