var loginM = angular.module('loginM', []);
loginM.controller('loginCtrl', ['$scope', '$rootScope', '$state', function($scope, $rootScope, $state){

    window.checkLoginStatus = function() {
      FB.getLoginStatus(function(response){
        console.log('YY');
        console.log(response);
        if (response.status === 'connected') {
          FB.api('/me', function(response) {
            console.log('Successful login for: ' + response.name);
            // document.querySelector('.fb-login-button').style.display = 'none';
            $rootScope.username = response.name;
            //$scope.state = 'filling';
            //$scope.$apply();
            console.log('XX');
            $state.go('form');
            $scope.$apply();
          });
        } else {
            $scope.message = response.status;
        }
      });
    };
    window.fbAsyncInit = function() {
      FB.init({
        appId      : '588525377965036',  //'588462391304668',
        cookie     : true,  // enable cookies to allow the server to access 
                            // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.5' // use graph api version 2.5
      });
      checkLoginStatus();
    };


    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.5&appId=588525377965036";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
}]);
