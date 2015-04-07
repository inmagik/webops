angular.module('angularWebops', [])
.factory('webopsHelpers', ['$q', function ($q) {
    
    var svc = {};
    svc.loadFile = function(key, fileMeta){
        var deferred = $q.defer();
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
    };


    svc.getParamsInfo = function(op){
        var out = { paramsRequired : {}, paramsOptional : {}, fileParams : {} };
        _.each(op.parameters, function(p, pname){

            if(p.type == 'FileField'){
                out.fileParams[pname] = p;
            } else {
                if(p.required){
                    out.paramsRequired[pname] = p;
                } else {
                    out.paramsOptional[pname] = p;
                }
            };
    
        });
        return out;
    };


    svc.prepareParams = function(params, filesData, filesUrls){
        var deferred = $q.defer();
        var jsond = {};
        var fileReads = [];

        angular.extend(jsond, params);
        
        _.each(filesData, function(value, key){
            fileReads.push(svc.loadFile(key, value))    
        });

        _.each(filesUrls, function(value, key){
            jsond[key] = { 'data' : value};
        });

        $q.all(fileReads)
        .then(function(results){
            _.each(results, function(result){
                angular.extend(jsond, result)
            });
            deferred.resolve(jsond);
        })

        return deferred.promise;


    }

    return svc;
}])
