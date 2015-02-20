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


.controller('OpCtrl', function ($scope, Restangular, op, $http, $timeout, $q) {
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
    $scope.filesUrls = { };

    $scope.readFile = function(name, $files){
        $timeout(function(){
            $scope.filesMeta[name] = $files[0];
            $scope.filesData[name] = $files[0];
        });
    };



    var loadFile = function(key, fileMeta){
        var deferred = $q.defer();
        console.log(1, fileMeta)
        var reader = new FileReader()
        reader.onload = function(e){
            console.log("e",reader.result);
            var out = {};
            out[key] = { 
                'data' : reader.result,
                'filename' : fileMeta.name,
                'mime' : fileMeta.type
            }
            deferred.resolve(out);
        };
        reader.onerror = function(err){
            deferred.reject(err);
        };
        reader.readAsDataURL(fileMeta);
        return deferred.promise;
    }

 
    
    /* this one uses json encoding */
    $scope.launch = function(){
        

        var jsond = {};
        var fileReads = [];

        $scope.data.processing =true;

        _.each($scope.paramsData, function(value, key){
            jsond[key] = value;
        })
        
        _.each($scope.filesData, function(value, key){
        
            fileReads.push(loadFile(key, value))    
        })

        _.each($scope.filesUrls, function(value, key){
        
            jsond[key] = { 'data' : value};
        })

        $q.all(fileReads)
        .then(function(results){
            _.each(results, function(result){
                angular.extend(jsond, result)
            });
            console.log("hs", jsond)

            $http.post(op.abs_url, jsond)
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



