function validate() {
    const uname = document.admin.username.value;
    if (uname == '') {
        document.getElementById('error').innerHTML = "Please enter username!";
        return false;
    } else {
        document.getElementById('error').innerHTML = "";
    }

    const pass = document.admin.password.value;
    if (pass == '') {
        document.getElementById('error').innerHTML = "Please enter password!";
        return false;
    } else {
        document.getElementById('error').innerHTML = "";
    }

}


function validateEdit() {
    const uname = document.upform.username.value;
    if (uname == '') {
        document.getElementById('error').innerHTML = '<p>Error log:</p><p style="color: red;">Enter username</p>';
        return false;
    } else {
        document.getElementById('error').innerHTML = '';
    }

    const regexp1 = new RegExp("[^a-z|^A-Z|^0-9|_|.]");
    if (regexp1.test(uname)) {
        document.getElementById('error').innerHTML = '<p>Error log:</p><p style="color: red;">Username should not contain whitespace and special characters!</p>';
        return false;
    } else {
        document.getElementById('error').innerHTML = '';
    }

    const password = document.upform.password.value;
    if (password.length < 8) {
        document.getElementById('error').innerHTML = '<p>Error log:</p><p style="color: red;">Length is less than 8</p>';
        return false;
    } else {
        document.getElementById('error').innerHTML = '';
    }

}

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});
