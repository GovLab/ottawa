{#
{% if session['usersession'] %}
// WE HAVE THE AUTH DATA.
noiRef.authWithCustomToken('{{session['usersession']}}', function(error, authData) {
  if (error) {
    console.log("Login Failed!", error);
  } else {
    console.log("Login Succeeded!", authData);
    userAuthData = authData;
    user = { 'family_name': '{{session['family_name']}}',
             'given_name': '{{session['given_name']}}',
             'picture': '{{session['picture']}}' };
    $('.username').text(user.given_name);
    $('.profile-img').attr('src', user.picture);
  	$('#greetings').show();
  	$('.login').hide();
  }
});
{% else %}
{% endif %}
#}