angular.module("WebOps")
.controller('AppCtrl', function ($scope) {
    
    
})


.controller('HomeCtrl', function ($scope, Restangular, ops) {
    $scope.ops = ops;
    $scope.filter = {op:null};
    
    

})


.controller('OpCtrl', function ($scope, Restangular, op, $http, $timeout, $q, webopsHelpers) {

    $scope.data = {
        currentOp : op,
        processing : false,
        result : null,
        errors : null
    };

    var info = webopsHelpers.getParamsInfo(op);
    angular.extend($scope.data, info);


    $scope.paramsData = {};
    $scope.filesData = {};
    $scope.filesUrls = { };

    $scope.readFile = function(name, $files){
        $timeout(function(){
            $scope.filesData[name] = $files[0];
        });
    };
    
    /* this one uses json encoding */
    $scope.launch = function(){
        

        var jsond = {};
        var fileReads = [];
        $scope.data.processing = true;

        webopsHelpers.prepareParams($scope.paramsData, $scope.filesData, $scope.filesUrls)
        .then(function(jsond){

            $http.post(op.abs_url, jsond, {timeout:300000})
            .then(function(resp){
                $timeout(function(){
                    $scope.data.errors = null;
                    $scope.data.result = resp.data;
                })
            })
            .catch(function(err){
                console.error(err);
                $timeout(function(){
                    $scope.data.errors = err.data;
                    $scope.data.result = null;
                })
            })
            .finally(function(){
                $timeout(function(){
                    $scope.data.processing = false;
                });
            });

            $timeout(function(){
                $scope.$apply();
            })

        })
        .catch(function(err){
            console.error(err)
        })

    };


    /* this one uses form encoding */
    $scope.launch2 = function(){
        

        var fd = new FormData();
        var jsond = {};
        
        _.each($scope.filesData, function(value, key){
            fd.append(key, value);    
            jsond[key] = value;
        })

        _.each($scope.paramsData, function(value, key){
            fd.append(key, value);    
            jsond[key] = value;
        })


        console.log(1, jsond);
        return;
        

        $scope.data.processing =true;
        $http.post(op.abs_url, fd, {
            //withCredentials: true,
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        //Restangular.all(op.url).post($scope.userData)
        .then(function(resp){
            console.log("wow!", resp);
            $timeout(function(){
                $scope.data.errors = null;
                $scope.data.result = resp.data;
            })
        })
        .catch(function(err){
            console.error(err);
            $timeout(function(){
                $scope.data.errors = err.data;
                $scope.data.result = null;
            })
        })
        .finally(function(){
            $timeout(function(){
                $scope.data.processing = false;
            });
        });

        $timeout(function(){
            $scope.$apply();
        })
        


    };

    $scope.downloadFile = function(){
        blobUtil.base64StringToBlob($scope.data.result.data)
          .then(function(blob){
            saveAs(blob, $scope.data.result.filename);  
          })
    };


    $scope.clearFile = function(key){
        delete $scope.filesData[key];
    }





})



