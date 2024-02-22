<?php

// Hello World!!!

$_parameters = $_GET;

header('Content-Type: application/json');

if(!empty($_parameters)){
    if(!empty($_parameters['ip'])){
        ipcheck($_parameters["ip"]);
    }
}
else{
    noParameters();
}

function noParameters(){
    echo json_encode(
        [
            "command" => "noParameters",
            "message" => "You Havent parameters for use API!",
            "reslut" => false
        ]
        );
    return;
}

function ipcheck($link){
    $url = "https://ipwho.is/$link";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    $ip = json_decode($response) -> ip;
    $success = json_decode($response) -> success;
    if($success == true){
        $img = json_decode($response) -> flag -> emoji;
        $country = json_decode($response) -> country;
        $conn = json_decode($response) -> connection -> isp;
        
        echo json_encode([
            "success" => true,
            "ip" => $ip,
            "Created By" => "@TheHeroAPI and @Mamad Mehrabi in telegram",
            "result" => [
                $response
            ]
        ]);
        return;
    }
    else{
        echo json_encode([
            "ip" => $ip,
            "result" => false,
            "message" => "Please Enter Your IP!!"
        ]);
    }
}