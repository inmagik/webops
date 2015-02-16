angular.module("WebOps")
.directive('appNavbar', [function () {
    return {
        restrict: 'A',
        templateUrl : 'templates/app_navbar.html',
        replace : true,
        link: function (scope, iElement, iAttrs) {
            
        }
    };
}])