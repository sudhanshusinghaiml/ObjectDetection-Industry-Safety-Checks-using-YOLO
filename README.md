# ObjectDetection-Industry-Safety-Checks-using-YOLO
Industry Safety check using Object Detection thru YOLO

### Important Reference for this project
- [Data link](https://drive.google.com/file/d/1ncxeLuWEMXkXVI79LXbA38s-Ij0d2q4E/view?usp=sharing)
- [Yolov7 Github repo link](https://github.com/WongKinYiu/yolov7)
- [Yolov7 Tutorial](https://youtube.com/playlist?list=PLkz_y24mlSJagh6O2MIrgI-Ki-t1rhjLI&si=6eMTgSe1-cbWVPGX)


### Workflows for this project
 - constants
 - config_entity
 - artifact_entity
 - components
 - pipeline
 - app.py


### How to run?

```bash
conda create -n object-detection-industry-safety-checks python=3.10.14 -y
```

```bash
conda activate object-detection-industry-safety-checks
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

# AWS-CICD-Deployment-with-Github-Actions

### 1. Login to AWS console.

### 2. Create IAM user for deployment with specific access

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws

### 3. How to setup Application on EC2: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	
### 4. Create ECR repo to store/save docker image
    - Save the URI: 136566696263.dkr.ecr.us-east-1.amazonaws.com/yolov7app

	
### 5. Create EC2 machine (Ubuntu) 

### 6. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
### 7. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


### 8. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = us-east-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app