var resultsM = angular.module('resultsM', []);
resultsM.controller('resultsCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
	$scope.results = $rootScope.results;
	console.log($scope.results);
}]);
