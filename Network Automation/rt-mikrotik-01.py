import paramiko
import time

# Connection details
ip_address = '172.11.0.2'
username = 'admin'
password = 'adaptive'

# Set up the SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the router
ssh_client.connect(hostname=ip_address, username=username, password=password)
print("Success login to {}".format(ip_address))

# Invoke an interactive shell session
conn = ssh_client.invoke_shell()
time.sleep(1)  # Allow shell session to initialize

# Send the command to the router (corrected command)
conn.send("ip address add address=192.168.1.2/24 interface=ether4\n")
time.sleep(2)  # Wait for the command to execute

# Receive the output from the shell
output = conn.recv(65535)  # Receive up to 65535 bytes of data

# Decode and print the output
print(output.decode('utf-8'))

# Close the SSH connection
ssh_client.close()
