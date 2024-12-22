# Randomness Beacon

## Files

There are three folders:

local folder is stored in local lab machine. MDB folder is stored on remote server as the backend. Webpage folder is stored on remote machine as the frontend. The frontend is hosted by Apache webserver on Ubuntu 22.04 LTS.

local/run.py : It has the code for randomness collection, pulse generation, and sending pulses to AWS server.

MDB/DatabaseTier/db.py : This file looks for the update of data.json. The data.json file is sent from the lab beacon machine.

MDB/DatabaseTier/db_var.py, MDB/ApplicationTier/db_var.py : This file contains the database variables of ip_address, database_name, collection_name. These variables are imported and used by the FastAPI server and db.py for interaction with the database.

MDB/ApplicationTier/routes.py, MDB/ApplicationTier/main.py, MDB/ApplicationTier/model.py : They launch the FastAPI to communicate with the MongoDB database.

MDB/DatabaseTier/data.json : An example json pulse data.

frontend : This folder contains the frontend files.

In addition to these files, the QRNG3 folder: https://qolah.org/repos/qrng3/ from s-15: https://s-fifteen.com/products/random-number-generator needs to be downloaded using subversion in linux, and stored in the local folder together with the run.py and labqrng.py.

A private key file for SSH connection and SCP command is required. This key file needs to be stored in the directory of local/Keypair/"...".pem

## Setting up the beacon.

The AWS servers setup:

Setup the environment from scratch: Using Ubuntu 22.04 OS as an example.

1. Create a new instance of remote machine on AWS.

2. SSH into the remote machine with the private key file "...".pem .

3. Install Miniconda or Anaconda on the remote machine :
   https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html 
   https://docs.anaconda.com/miniconda/miniconda-install/

   The Miniconda file can be downloaded using this link with either wget or curl command.
   https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
   https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

4. Create a virtual environment, differnet from the base environment.

Setup the frontend instance.

1. Install Apache webserver with the command below. The learning resources are listed below.
   <img width="779" alt="image" src="https://github.com/GitHub0b00/Randomness-Beacon/assets/173871648/f3a70b30-1818-4e6e-92f6-c186cc840783">
   https://medium.com/@KerrySheldon/ec2-exercise-1-1-host-a-static-webpage-9732b91c78ef
   https://ubuntu.com/tutorials/install-and-configure-apache#1-overview

2. Put the frontend files (webpage) onto the AWS machine.

3. Start the Apache webserver

4. Set the proxy in Apache webserver configuration file so that the incoming requests are redirected into the interna load balancer.

Setup the data tier instance

1. Install MongoDB on Ubuntu 22.04, following the procedure here:
   https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

2. Start the MongoDB process.

3. Setup a SSH session management tool called tmux.

4. Put the backend files (MDB) onto the AWS machine. The backend files can be stored in any place of the remote machine.

5. Define the correct (desired) database name and collection name in db_var.py.

6. Delete the data.json file in MDB folder.

7. Attach onto a tmux session.

8. Start db.py with the command: "python db.py" or "python3 db.py", in the backend (MDB) folder.

9. Detach from the current tmux session.

Setup the application tier instance

1. Setup the same SSH session management tool tmux.

2. Put the backend files (MDB) onto the AWS machine. The backend files can be stored in any place of the remote machine.

3. Define the correct (desired) database name and collection name in db_var.py.

4. Delete the data.json file in MDB folder.

5. Attach onto a tmux session.

6. In the backend (MDB) folder, start the FastAPI webserver by the command: "uvicorn main:app --host a.b.c.d --port xxxx --reload". The allowed incoming origins is set in the "main.py" file in the MDB folder.

7. Detach from the current tmux session.

--------------------------------------------------
Till here, the servers are setup.

Setup the local program:

1. On local lab laptop, setup the files in the local folder, put the qrng3 folder into the same directory as the files in the local folder.

2. Connect the S-15 QRNG and/or the lab QRNG

3. Start the data generating process with the command: "python run.py" in the local folder which has the file "run.py", the file "labqrng.py", the folder "Keypair", and the folder "qrng3".

## AWS

The web application is hosted on AWS. It was built with a 3-tier architecture to ensure availability and robustness. The components and their relationship with each other are displayed and labeled in the picture below.
<img width="1108" alt="AWSarchitecture" src="https://github.com/user-attachments/assets/047e8fcd-1f95-40df-a4f1-19aa99dda349">

In this AWS 3-tier web architecture diagram, the frontend files are ran by Apache Webserver on the frontend tier machine, the application tier files are ran by FastAPI on the application tier machine, the backend tier files are ran by MongoDB on the database tier machine.

Several settings in addition to the installation and launch of respective programs.

In the frontend machine, a proxy setting needs to be configured in the apache webserver configuration file in order to redirect incomming API requests to the application loadbalancer.

In the application tier machine, the ip address for db_var.py needs to be the private ip address of the database tier so that the FastAPI qurey to the MongoDB database on the database tier machine.

In the database tier machine, the bind_ip setting for the database needs to be the private ip of the machine rather than the default localhost 127.0.0.1

## Error handling
The main idea of error handlnig is to restart the service appropriatly so that the hash chain is intact. Hash chain and data fields documentation can be found in the NIST reference (https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8213-draft.pdf)

### If the lab program stops:

Go to the folder Documents/beacon/2024August16…/run.py in the beacon conda environment. => start the beacon python script with “python run.py”

After the command being excuted, two prompts will appear to ask for inputs on: Whether to start a new chain, and whether to use a new key pair. 

#### Whether to start a new chain: two options: “new” and “continue”

When “new” is typed, you enter a chain index

When “continue” is typed, a check on whether the previous pulse exists will be conducted by the program. If there is no previous pulse stored on local cache, a new chain will be started.

If the local data.json matches the latest pulse on the cloud display and if the next_locrand.pkl is the locrand corresponding to the current pulse. It is good to choose continue even there is a gap. If not, choose start a new chain. The idea is to decide if a hash chain is intact. This means checking if the previous pulse is intact, and check if the local random value is intact. How to check if the local random value is intact? Compute the SHA512 hash of the local random value.

#### Whether to use a new key pair: two options: “new” and “continue”

If a new key pair is chosen, you need to copy and backup the old key pair first, and record the last pulse that the old key is responsible for. This is needed for verification purpose.

To access the remote database: login onto the AWS account. Go to EC2 => instances =>  DatabaseEC2Instance1a => connect. This connects you to the AWS instance where the database runs. The connection is by either SSH or Session Manager. Other connection methods I have not tried.

### If the internet connection is broken but the lab program is running (meaning that the pulse is generated on the local machine but not sent to the remote machine): 
start a new chain.

### If there is problem with the AWS remote servers:

If presentation tier and the application tier are down: login onto them and restart the Apache webserver and / or the FastAPI application. For the FastAPI application, it currently runs on the tmux session. It listens to the localhost and the port number defined in the application load balancer on AWS. It is port 8000 at the moment.

If the database tier is down, update the collection name in “db_var.py” to a new collection, or a new database all together. Restart the mongoDB process in the tmux session.
![image](https://github.com/user-attachments/assets/023e756c-fca5-4fdf-b585-91f2e89a7650)

