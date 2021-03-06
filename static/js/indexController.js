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
    $scope.word = /^\s*\w*\s*$/;
    $scope.save = function() {
        url = "/action/post/settings/" + $scope.data.doc_id;
        $http.post(url, $scope.data.settings).success(function() {
            current_url = $window.location.href;
            current_doc = _.last(current_url.split("/"));
            if (current_doc != $scope.data.settings.handle) {
                $window.location.href = current_url.replace("/"+current_doc, "/"+$scope.data.settings.handle);
            }
        });
        analytics.track('Saved settings',
            {handle: $scope.data.settings.handle});
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
    $scope.new_open = function() {
        var picker = new google.picker.PickerBuilder().
            addView(google.picker.ViewId.DOCUMENTS).
            setCallback(pickerCallback).
            build();
        picker.setVisible(true);
    };
}
