var resultsM = angular.module('resultsM', ['ui.bootstrap']);

resultsM.controller('resultsCtrl', ['$scope', '$rootScope', '$uibModal', function($scope, $rootScope, $uibModal) {
	$scope.results = $rootScope.results;
	console.log($scope.results);

	$scope.open = function (num) {
		var modalInstance = $uibModal.open({
			animation: true,
			templateUrl: 'view/detail.html',
			controller: 'modalCtrl',
			size: 'lg',
			resolve: {
				item: function () {
					return $scope.results.results[num]
				}
			}
		});
	}


}]);

resultsM.controller('modalCtrl', ['$scope', '$uibModalInstance', 'item', function($scope, $uibModalInstance, item){
	$scope.item = item;

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

	$scope.status = {
		isFirstOpen: true,
		isFirstDisabled: false
	};


}]);
