# -*- coding:utf-8 -*-
# @Author  : 'longguangbin'
# @Contact : lgb453476610@163.com
# @Date    : 2018/12/28
"""  
Usage Of 'test_client_mode' : 
"""

import os
import sys

spark_sql = "spark-submit --master yarn --deploy-mode client" \
            " --num-executors 5" \
            " --executor-memory 5g" \
            " --executor-cores 5" \
            " --driver-memory 5g" \
            " --driver-cores 5" \
            " --conf spark.yarn.appMasterEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer" \
            " --conf spark.executorEnv.yarn.nodemanager.container-executor.class=DockerLinuxContainer" \
            " --conf spark.yarn.appMasterEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest" \
            " --conf spark.executorEnv.yarn.nodemanager.docker-container-executor.image-name=bdp-docker.jd.com:5000/wise_mart_cib:latest" \
            " --conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server" \
            " --conf spark.executorEnv.LD_LIBRARY_PATH=/software/servers/hadoop-2.7.1/lib/native:/software/servers/jdk1.8.0_121/jre/lib/amd64/server" \
            " {pyfile} {args}"

file1 = sys.argv[1]
print(spark_sql.format(pyfile=file1, args=''))
os.system(spark_sql.format(pyfile=file1, args=''))
