var formM = angular.module('formM', []);
formM.controller('formCtrl', ['$scope', '$http', '$rootScope', '$state', function($scope, $http, $rootScope, $state) {
	$scope.req = {
		'from': '',
		'budget': 300,
		'depart': null,
		'return': null,
	};
	$scope.message = '';
	$scope.submit = function(){
		var resP = $http.post('backend', $scope.req);
		$scope.message = 'Please wait...';
		resP.then(function(response){
			console.log(response);
			$rootScope.results = response.data;
			$rootScope.results.results.forEach(function(city){
				city.routes.forEach(function(route){
					route.cost = parseFloat(route.flight.fare.total_price) + parseFloat(route.hotel.total_price.amount);
				});
			});
			$state.go('results');
		});
	};
}]);
