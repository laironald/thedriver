var myApp = angular.module('myApp', []);
myApp.factory('Data', function() {
    return {};
});


function PreviewModalCtrl($scope, Data) {
    $scope.data = Data;
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
function SettingModalCtrl($scope, $window, $http, Data) {
    $scope.data = Data;
    $scope.save = function() {
        data = {"ron": "ron"};
        $http.post("/action/post/settings", data).success(function() {
            // $window.location.href = "/in/ghostie/testing";
        });
        analytics.track('Saved settings',
            {url: $scope.data.settings.handle});
    };
}

function MenuClickCtrl($scope, $http, Data) {
    $scope.data = Data;
    $scope.preview = function(data_url) {
        $scope.data.url = "/preview/" + data_url;
        $scope.data.action = 0;
        analytics.track('Previewed document',
            {url: $scope.data.url});
    };
    $scope.settings = function() {
        $http.get("/action/get/settings").success(function(data) {
            $scope.data.settings = data;
        });
    };
}