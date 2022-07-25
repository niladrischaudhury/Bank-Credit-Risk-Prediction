# Bank-Credit-Risk-Prediction
Predict Bank Credit Risk using South German Credit Data

# Project Requirements 
1. [Requirement Document](https://drive.google.com/file/d/1DgBcDSYCxdmoKFhxtlCN-5VGSZhLGOTC/view)
2. [Project Description](https://archive.ics.uci.edu/ml/datasets/South+German+Credit#)
3. [Project Data](https://archive.ics.uci.edu/ml/machine-learning-databases/00522/SouthGermanCredit.zip)


#### Creating conda environment
```
conda create -p venv python==3.7 -y
```
```
conda activate venv/
```
OR 
```
conda activate venv
```

#### Create Notebook Folder and install ipykernel to execute jupyter notebook
```
pip install ipykernel
```

#### Keep adding dependency in requirements.txt and run following command to install then in the virtual environment

```
pip install -r requirements.txt
```

#### Git Commands
#### To Add files to git
```
git add .
```

OR
```
git add <file_name>
```

> Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

To check the git status 
```
git status
```
To check all version maintained by git
```
git log
```

To create version/commit all changes by git
```
git commit -m "message"
```

To send version/changes to github
```
git push origin main
```

To check remote url 
```
git remote -v
```

### To setup CI/CD pipeline in heroku we need 3 information
1. HEROKU_EMAIL = niladri.schaudhury@gmail.com
2. HEROKU_API_KEY = <>
3. HEROKU_APP_NAME = bank-credit-risk-predictor

### Docker steps
#### BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```
> Note: Image name for docker must be lowercase


To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```

To check running container in docker
```
docker ps
```

Tos stop docker conatiner
```
docker stop <container_id>
```



```
python setup.py install
```


Install ipykernel

```
pip install ipykernel
```


Data Drift:
When your datset stats gets change we call it as data drift



## Write a function to get training file path from artifact dir