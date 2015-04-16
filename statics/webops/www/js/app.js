
angular.module("WebOps", ['ui.router', 'restangular', 'angularFileUpload', 'webops-angular'])

.config(function($stateProvider, $urlRouterProvider, $httpProvider, RestangularProvider){

    var baseServerUrl = '/';
    RestangularProvider.setBaseUrl(baseServerUrl);

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
        var newResponse;
        if (operation === "getList") {
            newResponse = response.results != undefined ? response.results : response;
            newResponse.metadata = {
              count : response.count,
              next : response.next,
              previous : response.previous
            }
        } else {
            newResponse = response;
        }
        return newResponse;
    });
  
    RestangularProvider.setRequestSuffix('/?');
    
    $urlRouterProvider.otherwise("/app");
    //
    // Now set up the states
    $stateProvider

    .state('home', {
      abstract : true,
      
      template : '<div ui-view></div>',
      resolve : {
        ops : function(Restangular){
          return Restangular.all('ops').getList();
        }
      }
    })

    .state('home.app', {
      url: "/app",
      templateUrl: "templates/home.html",
      controller  : 'HomeCtrl'
    })
    
    .state('home.op', {
      url: "/op/:opId",
      templateUrl: "templates/op.html",
      controller  :'OpCtrl',
      resolve : {
        op : function(ops, $stateParams){
          return _.find(ops, { id : $stateParams.opId })
        }
      }
      
    })

    .state('about', {
      url: "/about",
      templateUrl: "templates/op.html",
      controller  :'BooksCtrl'
      
    })



})
.run(function(){
    console.log("run here")
})