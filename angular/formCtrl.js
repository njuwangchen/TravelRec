var formM = angular.module('formM', []);
formM.controller('formCtrl', ['$scope', '$http', '$rootScope', '$state', '$timeout', function($scope, $http, $rootScope, $state, $timeout) {
	$scope.req = {
		'from': 'Chicago',
		'budget': 1000,
		'depart': null,
		'return': null,
	};
	$scope.message = '';
	$scope.submit = function(){
		if ($scope.planForm.$invalid) {
			console.log('invalid submittion');
			return;
		}
		var resP = $http.post('backend', $scope.req);
		// $scope.message = 'Please wait...';
		$scope.eta = 120;
		$scope.clock = $timeout(function(){
			$scope.message = ($scope.eta--) + ' seconds remaining';
			console.log($scope.message);
		}, 1000);
		$scope.planForm.disabled = true;
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
