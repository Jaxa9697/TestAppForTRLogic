

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendPost(url, data, error) {
    $.post(
        url,
        data,
        function(response) {
            if (!response.status) {
                let data = response.message;
                Object.keys(data).forEach(function (key) {
                    error.html(key + ': ' + data[key].toString());
                });
            } else {
                $(location).attr('href', response.message);
            }
      }
    ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
    });
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    }
});

jQuery(document).ready(function() {

    $('.input-group.date').datepicker({
        startView: 2
    });

  $('#logIn').on('submit', function (event) {

      event.preventDefault();
      let username = $('#username').val(),
          password = $('#password').val(),
          error = $('.errorLogin').eq(0);

      sendPost('/login/' ,
             { 'username': username, 'password': password },
                  error);
  });

  $('#signUp').on('submit', function (event) {

      event.preventDefault();
      let username = $('#login'),
          email = $('#email'),
          password1 = $('#password1'),
          password2 = $('#password2');

      let fd_login = $('#fd-login'),
          fd_email = $('#fd-email'),
          fd_password = $('#fd-password');

      username.removeClass('is-invalid');
      email.removeClass('is-invalid');
      password1.removeClass('is-invalid');
      password2.removeClass('is-invalid');

      if (password1.val() !== password2.val()) {
          password2.addClass('is-invalid');
      } else {
          $.post(
              '/signup/',
              {
                  'username': username.val(),
                  'email': email.val(),
                  'password1': password1.val(),
                  'password2': password2.val()
              },
              function(response) {
                  if (!response.status) {
                      let data = response.message;
                      Object.keys(data).forEach(function (key) {
                          if (key === 'username') {
                              username.addClass('is-invalid');
                              fd_login.html(data[key]);
                          }

                          if (key === 'email') {
                              email.addClass('is-invalid');
                              fd_email.html(data[key]);
                          }

                          if (key === 'password2') {
                              password2.addClass('is-invalid');
                              fd_password.html(data[key]);
                          }
                      });
                  } else {
                      $(location).attr('href', response.message);
                  }
              }
          ).fail(function(jqXHR, textStatus, err) {
              alert('text status ' + textStatus + ', err ' + err)
          });
      }
  });

  $('#changePassword').on('submit', function (event) {

      event.preventDefault();
      let old_password = $(this).find('input[name="old_password"]').eq(0),
          new_password1 = $(this).find('input[name="new_password1"]').eq(0),
          new_password2 = $(this).find('input[name="new_password2"]').eq(0);

      let fd_old_password = $('#fd-old-password'),
          fd_new_password = $('#fd-new-password');

      old_password.removeClass('is-invalid');
      new_password2.removeClass('is-invalid');

      if (new_password1.val() !== new_password2.val()) {
          new_password2.addClass('is-invalid');
      } else {
          $.post(
              '/changePassword/',
              $(this).serialize(),
              function(response) {
                  if (!response.status) {
                      let data = response.message;
                      Object.keys(data).forEach(function (key) {
                          if (key === 'old_password') {
                              old_password.addClass('is-invalid');
                              fd_old_password.html(data[key]);
                          }

                          if (key === 'new_password2') {
                              new_password2.addClass('is-invalid');
                              fd_new_password.html(data[key]);
                          }
                      });
                  } else {
                      alert(response.message);
                      old_password.val('');
                      new_password1.val('');
                      new_password2.val('');
                  }
              }
          ).fail(function(jqXHR, textStatus, err) {
              alert('text status ' + textStatus + ', err ' + err)
          });
      }
  });

});