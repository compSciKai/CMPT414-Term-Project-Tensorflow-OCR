<!DOCTYPE html>
<html>
<title>SFU CMPT414 OCR Project</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
.w3-row-padding img {margin-bottom: 12px}
/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 120px;background: #222;}
/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
#main {margin-left: 120px}
/* Remove margins from "page content" on small screens */
@media only screen and (max-width: 600px) {#main {margin-left: 0}}
</style>
<body>

<?php
 /**
 * Sample code for the GetRates Canada Post service.
 *
 * The GetRates service returns a list of shipping services, prices and transit times
 * for a given item to be shipped.
 *
 * This sample is configured to access the Developer Program sandbox environment.
 * Use your development key username and password for the web service credentials.
 *
 **/

// Your username, password and customer number are imported from the following file
// CPCWS_Rating_PHP_Samples\REST\rating\user.ini
$userProperties = parse_ini_file(realpath(dirname($_SERVER['SCRIPT_FILENAME'])) . '/../user.ini');

$username = $userProperties['username'];
$password = $userProperties['password'];
$mailedBy = $userProperties['customerNumber'];


// REST URL
$service_url = 'https://ct.soa-gw.canadapost.ca/rs/ship/price';

// Create GetRates request xml
$originPostalCode = $_POST["o-code"]; //'H2B1A0';
$postalCode = $_POST["d-code"]; // 'K1K4T3';
$weight = 0.3;
$date = date("Y-m-d"); //'2020-04-09';
$quote = 'counter';

$xmlRequest = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
  <quote-type>{$quote}</quote-type>
  <expected-mailing-date>{$date}</expected-mailing-date>
  <parcel-characteristics>
    <weight>{$weight}</weight>
  </parcel-characteristics>
  <origin-postal-code>{$originPostalCode}</origin-postal-code>
  <destination>
    <domestic>
      <postal-code>{$postalCode}</postal-code>
    </domestic>
  </destination>
</mailing-scenario>
XML;

$curl = curl_init($service_url); // Create REST Request
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2);
curl_setopt($curl, CURLOPT_CAINFO, realpath(dirname($_SERVER['SCRIPT_FILENAME'])) . '/../../../third-party/cert/cacert.pem');
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $xmlRequest);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($curl, CURLOPT_USERPWD, $username . ':' . $password);
curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/vnd.cpc.ship.rate-v4+xml', 'Accept: application/vnd.cpc.ship.rate-v4+xml'));
$curl_response = curl_exec($curl); // Execute REST Request
if(curl_errno($curl)){
	echo 'Curl error: ' . curl_error($curl) . "<br>";
}

echo 'HTTP Response Status: ' . curl_getinfo($curl,CURLINFO_HTTP_CODE) . "<br><br>";

curl_close($curl);

// Example of using SimpleXML to parse xml response
libxml_use_internal_errors(true);
$xml = simplexml_load_string('<root>' . preg_replace('/<\?xml.*\?>/','',$curl_response) . '</root>');
if (!$xml) {
	echo 'Failed loading XML' . "<br>";
	echo $curl_response . "<br>";
	foreach(libxml_get_errors() as $error) {
		echo "\t" . $error->message;
	}
} else {
	if ($xml->{'price-quotes'} ) {
		$priceQuotes = $xml->{'price-quotes'}->children('http://www.canadapost.ca/ws/ship/rate-v4');
		if ( $priceQuotes->{'price-quote'} ) {
			foreach ( $priceQuotes as $priceQuote ) {
				echo 'Service Name: ' . $priceQuote->{'service-name'} . "<br>";
				echo 'Price: ' . $priceQuote->{'price-details'}->{'due'} . "<br>";
				echo 'Estimated Delivery Date: ' . $priceQuote->{'service-standard'}->{'expected-delivery-date'} . "<br><br>";
			}
		}
	}
	if ($xml->{'messages'} ) {
		$messages = $xml->{'messages'}->children('http://www.canadapost.ca/ws/messages');
		foreach ( $messages as $message ) {
			echo 'Error Code: ' . $message->code . "<br>";
			echo 'Error Msg: ' . $message->description . "<br><br>";
		}
	}

}

?>
<button class="w3-button w3-light-grey w3-padding-large" onclick="goBack()">
  <i class="fa fa-chevron-left"></i> GO BACK
</button>
</body>

<script>
  function goBack() {
    window.history.back();
  }
</script>
</html>
