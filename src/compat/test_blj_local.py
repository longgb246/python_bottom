# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/26
"""  
Usage Of 'test_blj_local' : 
"""

### bca
# "spark-submit --master yarn --deploy-mode cluster" \
# " --num-executors 40" \
# " --executor-memory 20g" \
# " --executor-cores 5" \
# " --driver-memory 20g" \
# " --driver-cores 12" \
# " --conf spark.yarn.appMasterEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer" \
# " --conf spark.executorEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer" \
# " --conf spark.yarn.appMasterEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest" \
# " --conf spark.executorEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest" \
# " --conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server" \
# " --conf spark.executorEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server" \
# " --py-files {zip_files}" \
# " {pyfile}  {args}"
#### jdvl start -m /data0/mart_bca:/data0/mart_bca:rw -i bdp-docker.jd.com:5000/wise_mart_bca:latest -o='--net=host' -I bash
# pyspark --master yarn \
# --num-executors 10 \
# --executor-memory 10g \
# --executor-cores 4 \
# --driver-memory 10g \
# --conf spark.driver.maxResultSize=20g \
# --conf spark.yarn.appMasterEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer \
# --conf spark.executorEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer \
# --conf spark.yarn.appMasterEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest \
# --conf spark.executorEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest \
# --conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server \
# --conf spark.executorEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server


# docker = "jdvl start -i bdp-docker.jd.com:5000/wise_mart_cmo_ipc_hecate -o='--net=host' -- python /home/cmo_ipc/zhanchangfei/KPI.py {0} {1} {2} {3} {4}".format(filepath, outpath, costpath, skucate, grossprofit)
# os.system(docker)

import os

t_path = os.path.abspath(os.path.dirname(__file__))

t_user = os.popen('whoami').readlines()[0].replace('\n', '')
t_mount = '/data0/{user}:/data0/{user}:rw'.format(user=t_user)  # 挂载
t_mirror = 'bdp-docker.jd.com:5000/wise_mart_bca:latest'  # 镜像

docker = "jdvl start -m {mount} -i {mirror} -o='--net=host' " \
         "-- python {t_path}/docx_report.py {t_path}". \
    format(mount=t_mount, mirror=t_mirror, t_path=t_path)

print(docker)
os.system(docker)
