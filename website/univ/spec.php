<?php  

require("header.php");

$path=$root_path."spec-xml/pred";

{
	
	$univ=$_GET['univ'];
	$prov=$_GET['prov'];
	$type=$_GET['type'];
	if($type=='-s')
	{
		$score=$_GET['score'];
		$tags=$_GET['tags'];
	}
		
	else
	{
		$score="";
		$tags="";
	}

	passthru($path." ". $prov." ".$type." ".$univ." ".$score." " . $tags." \"#\"");
	
}

?> 
