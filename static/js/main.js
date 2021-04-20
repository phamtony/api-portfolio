var delete_btns = document.querySelectorAll('.btn-danger');

for (var btn of delete_btns) {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (window.confirm('Delete Info?')) {
            window.location = e.target.parentElement.href;
        }
    });
}