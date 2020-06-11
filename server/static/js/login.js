function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    localStorage['Name'] = profile.getName();
  }