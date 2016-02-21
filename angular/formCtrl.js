var formM = angular.module('formM', []);
formM.controller('formCtrl', ['$scope', '$http', '$rootScope', '$state', '$interval', function($scope, $http, $rootScope, $state, $interval) {
	$scope.req = {
		'from': 'Chicago',
		'budget': 1000,
		'depart': null,
		'return': null,
	};
	$scope.message = '';
	$scope.fetching = false;
	$scope.submit = function(){
		if ($scope.planForm.$invalid) {
			console.log('invalid submittion');
			return;
		}
		if ($scope.fetching) {
			console.log('already fetching');
			return;
		}
		$scope.fetching = true;
		var resP = $http.post('/demo/', $scope.req);
		// $scope.message = 'Please wait...';
		$scope.eta = 120;
		$scope.clock = $interval(function(){
			$scope.message = ($scope.eta--) + ' seconds remaining';
			console.log($scope.message);
		}, 1000, $scope.eta);
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
