<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

use App\Http\Controllers\UploadController;

Route::post('/upload', [UploadController::class, 'store']);
Route::get('/results/{filename}', [UploadController::class, 'downloadResult']);
