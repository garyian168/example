<?php
//姓名库
$names=array(
    "Angle",
    "Bob",
    "Chris",
    "Devid",
    "Edison",
    "Felim",
    "Geroge",
    "Halen",
    "Iris",
    "Jack",
    "Kennedy",
    "Lily",
    "Moncia",
    "Nick",
    "Oliver",
    "Paul",
    "Queen",
    "Robert",
    "Stiff",
    "Tina",
    "Una",
    "Vicky",
    "Will",
    "Xander",
    "Yusuf",
    "Zoe"
    );
//获取GET提交参数
$n=$_GET["n"];

//对输入的姓名进行匹配查找
if (!empty($n))
{
    $nameResult="";
    foreach ($names as $name) {
        if(mb_stripos($name,$n) !== false){
            //累计所有匹配的姓名
            $nameResult .=$name.",";
        }
    }
    //移除最后一个，号
    $nameResult=mb_substr($nameResult,0,-1);
}

//输出匹配结果
if (empty($nameResult)){
    $result="目前没有匹配项";
}else{
    $result="您要查找的可能是：".$nameResult;
}

echo $result;
?>

