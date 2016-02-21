/**
 * Created by ClarkWong on 20/2/16.
 */

var routerApp = angular.module('routerApp', ['ui.router', 'ui.bootstrap', 'formM', 'resultsM']);

routerApp.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/form');
    $stateProvider
        .state('form', {
            url: '/form',
            views: {
                '': {
                    templateUrl: 'view/form.html'
                }
            }
        })
        .state('results', {
            url: '/results',
            views: {
                '': {
                    templateUrl: 'view/results.html'
                }
            }
        })
}]);
