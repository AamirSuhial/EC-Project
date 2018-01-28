<?php
if(isset($_POST['submit']) && !empty($_POST['image_url']) ){
	
	$image_url = $_POST['image_url'];
	
	$key = 'a629614d2e5845bbb45a46415143d74c';

	$ar =	array("inputs" => array("data" => array("image" => array("url" => "$image_url"))));
	
	$data=  '{
		"inputs": [
		  {
			"data": {
			  "image": {
				"url": "'.$image_url.'"
			  }
			}
		  }
		]
	  }';
	 $ch = curl_init('https://api.clarifai.com/v2/models/' . 'aaa03c23b3724a16a56b629203edc62c'. '/outputs'); 
			curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");  
			curl_setopt($ch, CURLOPT_POSTFIELDS, $data); 
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
			curl_setopt($ch, CURLOPT_HTTPHEADER, array(               
		"Authorization: Key $key",                                                                                
		"Content-Type: application/json")                                                                       
	);      
       
	
	    $output = curl_exec($ch); 
        curl_close($ch);   
		$output = json_decode($output, TRUE);
		
		$result = "Analyzed url = ".$image_url."<br />";
		$result .= "Found Following things with accuracy <br /><br />";
	
			foreach($output['outputs'][0]['data']['concepts'] as $value ){
				$result .= $value['name'].' - '.number_format(($value['value'] * 100 ),2).'%<br />';
			}
	
	echo $result;
	
	exit();
}	

?>
		
<html>
<head>
</head>
<body>
<form action="index.php" method="post">
<input type="text" value="http://images.all-free-download.com/images/graphiclarge/beautiful_nature_landscape_02_hd_picture_166206.jpg" placeholder="Image URL" name="image_url" />
<input type="submit" value="submit" name="submit" />
</form>
</body>
</html>