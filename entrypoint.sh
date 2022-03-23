#!/bin/bash

echo "120.133.64.93  git.xiaoyanggroup.cn" >>/etc/hosts
#flask run -h 0.0.0.0 -p 9998
python -m flask run -h 0.0.0.0 -p 9998