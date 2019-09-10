
systemctl daemon-reload
systemctl restart bbs
systemctl restart bbs-message-queue
systemctl restart nginx

echo 'succsss'
echo 'ip'
hostname -I
curl http://localhost
