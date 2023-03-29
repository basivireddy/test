1. Terraform installation

```
tfenv

git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile

tfenv install 0.14.9 
tfenv use 0.14.9
```

2. Ruby Installation 

```
rbenv
apt install rbenv
rbenv init
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'eval "$(~/.rbenv/bin/rbenv init - bash)"' >> ~/.bash_profile

gem install json -v '2.6.3'
apt install ruby-dev

rbenv install -L
rbenv install 2.7.1
rbenv global 2.7.1
```

3. Kitchen Installation

```
cd kitchen-test
gem install bundler
bundle install
```

4. Copy service account key file to fixtures/serviceaccounts folder
5. Login gcloud cli for kitchen verify because here we are verifying with gcloud cli.

    ```
    gcloud auth login 
    ```
6. Kitech commands

```
kitchen create   --> terraform init
kitchen converge  --> terraform apply
kitchen verify   
kitchen destroy  ---> terraform destroy
```
