if [ "`ls -A /opt/marioips/log/post_error/`" = "" ];
then
        echo "/opt/marioips/log/post_error/ is empty"
else
  for error_file in /opt/marioips/log/post_error/*
  do
    check_results=`curl -F "clientfile=@$error_file" -H "Accept: application/json" https://remoteadd:5000/api/evefile -k`
    if [[ $check_results =~ "success" ]]
    then
      echo "repost $error_file success"
      mv $error_file /opt/marioips/log/post_success/
    else
      echo "repost $error_file file"
    fi
  done
fi
