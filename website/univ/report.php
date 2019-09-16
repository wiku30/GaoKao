<?php  

require("header.php");

$path=$root_path."c-bin/search";


	
$province=$_GET['province'];
$score=$_GET['score'];
$spec=$_GET['spec'];

$tags=$_GET['tag1']." and ".$_GET['tag2'];

$prov_no['BeiJing']=0;
$prov_no['HuBei']=1;
$prov_no['HeiLongJiang']=2;
$prov_no['LiaoNing']=3;

if($score >=520 && $score <=720)
{
	if($spec=="")
		passthru($path." ".$province." ".$score." ".$tags." \"#\"");
	else
		Header("Location: spec.php?univ=".$spec."&prov=".$prov_no[$province]."&type=-s&score=".$score."&tags=".$tags);  
}
else
{
	echo "<h1>分数不在范围内！</h1>";
}
	


?> 

