def get_dummy_container_info():
	return {
             "Id": ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(20)),
             "Names":["/boring_feynman"],
             "Image": "ubuntu:latest",
             "ImageID": ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(64)),
             "Command": "echo 1",
             "Created": 1367854155,
             "Status": "Exit 0",
             "Ports": [{"PrivatePort": 2222, "PublicPort": 3333, "Type": "tcp"}],
             "Labels": {
                     "com.example.vendor": "Acme",
                     "com.example.license": "GPL",
                     "com.example.version": "1.0"
             },
             "SizeRw": 12288,
             "SizeRootFs": 0,
             "NetworkSettings": {
                     "Networks": {
                             "bridge": {
                                      "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                                      "EndpointID": "2cdc4edb1ded3631c81f57966563e5c8525b81121bb3706a9a9a3ae102711f3f",
                                      "Gateway": "172.17.0.1",
                                      "IPAddress": "172.17.0.2",
                                      "IPPrefixLen": 16,
                                      "IPv6Gateway": "",
                                      "GlobalIPv6Address": "",
                                      "GlobalIPv6PrefixLen": 0,
                                      "MacAddress": "02:42:ac:11:00:02"
                              }
                     }
             }
     }