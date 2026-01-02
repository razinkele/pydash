document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('pushmenu-toggle');
  if (btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      document.body.classList.toggle('sidebar-collapse');
    });
  }
});
