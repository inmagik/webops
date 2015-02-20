angular.module("WebOps")
.controller('AppCtrl', function ($scope) {

    $scope.globalMethod = function(){
        console.log(1);
    };

    
    
})


.controller('HomeCtrl', function ($scope, Restangular, ops) {
    $scope.ops = ops;
    $scope.filter = {op:null};
    
    

})


.controller('OpCtrl', function ($scope, Restangular, op, $http, $timeout) {
    console.log(op)    
    $scope.data = {
        currentOp : op,
        fileParams : {},
        paramsRequired : {},
        paramsOptional : {},
        processing : false,
        result : null,
        errors : null
    };

    _.each(op.parameters, function(p, pname){
        

        if(p.type == 'FileField'){
            $scope.data.fileParams[pname] = p;
        } else {
            if(p.required){
                $scope.data.paramsRequired[pname] = p;
            } else {
                $scope.data.paramsOptional[pname] = p;
            }
        };
    })

    $scope.paramsData = {};
    $scope.filesData = {};
    $scope.filesMeta = {};

    $scope.readFile = function(name, $files){
        $timeout(function(){
            $scope.filesMeta[name] = $files[0];
            $scope.filesData[name] = $files[0];
        });
    };

    $scope.launch = function(){
        

        var fd = new FormData();
        _.each($scope.filesData, function(value, key){
            fd.append(key, value);    
        })

        _.each($scope.paramsData, function(value, key){
            fd.append(key, value);    
        })
        

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
        console.log(1, $scope.data.result)
        blobUtil.base64StringToBlob($scope.data.result.data)
          .then(function(blob){
            saveAs(blob, $scope.data.result.filename);  
          })
    };


    $scope.clearFile = function(key){
        delete $scope.filesData[key];
    }





})



