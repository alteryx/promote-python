bash yum install -y graphviz
if [ -d /root/miniconda3 ]; then export PATH=/root/miniconda3/bin:$PATH; fi
pip install --upgrade pip
