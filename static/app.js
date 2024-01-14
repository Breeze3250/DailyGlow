function extend(button) {
    button.nextElementSibling.classList.toggle('hide');
}

function unextend(button) {
    button.parentElement.parentElement.classList.toggle('hide')
}

function remove(id, timestamp, path) {
    fetch(`/reminders/${path}/${timestamp}`, { method: 'DELETE' })
    document.getElementById(id).remove()
}

function validate_password() {
    let password = document.getElementById('password').value;
    let confirmpassword = document.getElementById('confirmpassword').value;
    if (password != confirmpassword) {
        document.getElementById('wrong_pass_alert').style.color = 'red'
        document.getElementById('wrong_pass_alert').innerHTML = "Passwords Do Not Match";
        document.getElementById('create').disabled = true;
        document.getElementById('create').style.opacity = (0.4);
    } else {
        document.getElementById('wrong_pass_alert').style.color = 'green';
        document.getElementById('wrong_pass_alert').innerHTML = 'Password Matched';
        document.getElementById('create').disabled = false;
        document.getElementById('create').style.opacity = (1)
    }
}