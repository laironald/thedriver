var myApp = angular.module('myApp', []);
myApp.factory('Data', function() {
    return {};
});


function PreviewModalCtrl($scope, Data) {
    $scope.data = Data;
    $scope.preview = function() {
        $scope.data.url = "/preview/" + $scope.data.doc_id;
        $scope.data.action = 0;
        analytics.track('Change preview option',
            {url: $scope.data.url});
    };
    $scope.publish = function() {
        $scope.data.url = "/view/" + $scope.data.doc_id;
        $scope.data.action = 1;
        analytics.track('Change preview option',
            {url: $scope.data.url});
    };
}
function SettingModalCtrl($scope, $window, $http, Data) {
    $scope.data = Data;
    $scope.save = function() {
        data = {"ron": "ron"};
        url = "/action/post/settings/" + $scope.data.doc_id;
        $http.post(url, data).success(function() {
            // $window.location.href = "/in/ghostie/testing";
        });
        analytics.track('Saved settings',
            {url: $scope.data.settings.handle});
    };
}
function MenuClickCtrl($scope, $http, Data) {
    $scope.data = Data;
    $scope.preview = function(doc_id) {
        $scope.data.doc_id = doc_id;
        $scope.data.url = "/preview/" + $scope.data.doc_id;
        $scope.data.action = 0;
        analytics.track('Previewed document',
            {url: $scope.data.url});
    };
    $scope.settings = function(doc_id) {
        $scope.data.doc_id = doc_id;
        url = "/action/get/settings/" + $scope.data.doc_id;
        $http.get(url).success(function(data) {
            $scope.data.settings = data;
        });
    };
}
