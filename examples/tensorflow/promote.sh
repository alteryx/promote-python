#curl -L https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh  > Miniconda.sh
curl -L https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh  > Miniconda.sh
if [ -d /root/miniconda3 ]; then rm -fR /root/miniconda3; fi
bash Miniconda.sh -b -p /root/miniconda3
bash yum install -y graphviz
export PATH=/root/miniconda3/bin:$PATH
pip install --upgrade pip
