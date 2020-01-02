#!/usr/bin/php -d open_basedir=/usr/syno/bin/ddns
<?php
if ($argc !== 5) {
    echo 'badparam';
    exit();
}
$account = (string)$argv[1];
$pwd = (string)$argv[2];
$hostname = (string)$argv[3];
$ip = (string)$argv[4];
if (strpos($hostname, '.') === false) {
    echo 'badparam';
    exit();
}
if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
    echo "badparam";
    exit();
}

$multiCurl = array();
$result = array();
$mh = curl_multi_init();

$array_1 = explode(',', $account);
foreach ($array_1 as $i => $id) {
    $url = 'https://dynamicdns.park-your-domain.com/update?host='.$id.'&domain='.$hostname.'&password='.$pwd.'&ip='.$ip;
    $multiCurl[$i] = curl_init();
    curl_setopt($multiCurl[$i], CURLOPT_URL, $url);
    curl_setopt($multiCurl[$i], CURLOPT_RETURNTRANSFER, true);
    curl_multi_add_handle($mh, $multiCurl[$i]);
}
$index=null;
do {
  curl_multi_exec($mh,$index);
} while($index > 0);
foreach($multiCurl as $k => $ch) {
  $result[$k] = curl_multi_getcontent($ch);
  $res = $result[$k];
  $xml = new SimpleXMLElement($res);
  if ($xml->ErrCount > 0) {
      $error = $xml->errors[0]->Err1;
      if (strcmp($error, "Domain name not found") === 0) {
          echo "nohost";
      } elseif (strcmp($error, "Passwords do not match") === 0) {
          echo "badauth";
      } elseif (strcmp($error, "No Records updated. A record not Found;") === 0) {
          echo "nohost";
      } else {
          echo "911 [".$error."]";
      }
  } else {
      echo "good";
  }
  curl_multi_remove_handle($mh, $ch);
}
curl_multi_close($mh);
