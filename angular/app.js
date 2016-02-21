/**
 * Created by ClarkWong on 20/2/16.
 */

var routerApp = angular.module('routerApp', ['ui.router', 'ui.bootstrap', 'ngAnimate', 'formM', 'resultsM', 'loginM']);

routerApp.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/login');
    $stateProvider
        .state('login', {
            url: '/login',
            views: {
                '': {
                    templateUrl: 'view/login.html'
                }
            }
        })
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
