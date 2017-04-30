var app = angular.module("app", ['ngRoute','ngResource']);

app.controller('mainController',function($scope){
	$scope.name='rafik';
	$scope.fullname='md rafik kamal';
});
