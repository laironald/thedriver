var myApp = angular.module('myApp', []);
myApp.factory('Data', function() {
    return {"action": 0};
});


function PreviewCtrl($scope, Data) {
    $scope.data = Data;
    console.log($scope.data);
    $scope.preview = function(data_url) {
        $scope.data.url = "/preview/" + data_url;
        $scope.data.action = 0;
        analytics.track('Change preview option',
            {url: $scope.data.url});
    };

    $scope.publish = function(data_url) {
        $scope.data.url = "/view/" + data_url;
        $scope.data.action = 1;
        analytics.track('Change preview option',
            {url: $scope.data.url});
    };
}

function MenuClickCtrl($scope, Data) {
    $scope.data = Data;
    $scope.preview = function(data_url) {
        $scope.data.url = "/preview/" + data_url;
        $scope.data.action = 0;
        analytics.track('Previewed document',
            {url: $scope.data.url});
    };
}