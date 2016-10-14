<?php
	// 服务器端为格林尼治标准时间，这里需设置为中国所在时区
	date_default_timezone_set("PRC");

	$username = null;
	$ajaxMethod = null;
	
	// 判断是 GET 还是 POST
	if(isset($_GET["username"])) {
		$username = $_GET["username"];
		$ajaxMethod = "GET";
	} else {
		$username = $_POST["username"];
		$ajaxMethod = "POST";
	}

	echo "你好 ，" . $username . ", 现在时间为：" . date("Y-m-d H:i:s"). "，此数据来源于 " . $ajaxMethod . " Ajax";
?>