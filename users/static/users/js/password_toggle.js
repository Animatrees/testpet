document.querySelectorAll('.toggle-password').forEach(function(button) {
  button.addEventListener('click', function() {
    var targetInput = document.getElementById(this.getAttribute('data-target'));
    if (targetInput.type === 'password') {
      targetInput.type = 'text';
      this.innerHTML = '&#x1f31d;';
    } else {
      targetInput.type = 'password';
      this.innerHTML = '&#x1f31a;';
    }
  });
});