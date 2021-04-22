var delete_btns = document.querySelectorAll('.btn-danger');

for (var btn of delete_btns) {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (window.confirm('Delete Info?')) {
            window.location = e.target.parentElement.href;
        }
    });
}

function generateAPI(length) {
    var result           = [];
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result.push(characters.charAt(Math.floor(Math.random() *
 charactersLength)));
   }
   return result.join('');
}

document.getElementById('api_button').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('api_key').value = generateAPI(24)
});