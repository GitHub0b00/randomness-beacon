For local.py file, in the file uploading line, please update the scp command: Update the local file path to be the path that has the word.txt file. Update the key file to be the current key file in use. Update the server address in the scp command to be the current server address and update the target folder to be the current folder that contains the streaming webpage.

Current frontend server ip: 47.129.236.129

Current streaming frontend folder: /var/www/web/streaming

In the case that more than one frontend server is deployed with application load balancer. The upload should be done with multiple target servers. Or, it is better if the use of Amazon S3 hosting can be explored.
