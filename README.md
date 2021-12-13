# Lab 07

## Hadoop Setup

   * Install prerequisites:

```
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre
sudo apt install openssh-server openssh-client
```
   * Setup a user for Hadoop:

```
sudo adduser --gecos "" hadoop
xhost +
```
   
   * Switch to the Hadoop user: `su hadoop`
   * Download and extract Hadoop:

```
cd ~
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xvzf hadoop-3.3.1.tar.gz
```

   * Get Hadoop configuration files:

```
cd ~/hadoop-3.3.1/etc/hadoop/
wget https://raw.githubusercontent.com/GENBUS760/Lab07/master/hadoop-config/core-site.xml -O core-site.xml
wget https://raw.githubusercontent.com/GENBUS760/Lab07/master/hadoop-config/hdfs-site.xml -O hdfs-site.xml
wget https://raw.githubusercontent.com/GENBUS760/Lab07/master/hadoop-config/mapred-site.xml -O mapred-site.xml
wget https://raw.githubusercontent.com/GENBUS760/Lab07/master/hadoop-config/yarn-site.xml -O yarn-site.xml
wget https://raw.githubusercontent.com/GENBUS760/Lab07/master/hadoop-config/hadoop-env.sh -O hadoop-env.sh
```

   * Setup SSH keys for the Hadoop user:

```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

   * Test SSH keys for Hadoop user:

```
ssh localhost
exit
```

   * Create directories needed by Hadoop:

```
mkdir ~/hadooptmpdata
mkdir -p ~/hdfs/namenode ~/hdfs/datanode
```

   * Copy-paste the following at the end of ~/.bashrc (`gedit ~/.bashrc`):

```
export HADOOP_HOME=/home/hadoop/hadoop-3.3.1
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

   * Then run: `source ~/.bashrc; echo $HADOOP_HOME`
   * Format the NameNode: `hdfs namenode -format`
   * Start HDFS: `start-dfs.sh`
   * Start YARN: `start-yarn.sh`
   * Check Java processes: `jps`. You will see something like:

```
12368 DataNode
12737 ResourceManager
12868 NodeManager
12565 SecondaryNameNode
13112 Jps
12200 NameNode
```

## Running a MapReduce job

   * Switch to the Hadoop user (if you are not already): `su hadoop`
   * Get the data and MapReduce code:

```
cd ~
git clone https://github.com/GENBUS760/Lab07.git 
cd Lab07 
```

   * Copy the ledger data to HDFS:

```
hadoop fs -put ledger.txt /
hadoop fs -ls /
hadoop fs -tail /ledger.txt

hadoop fs -mkdir /myinput
hadoop fs -mv /ledger.txt /myinput/ledger.txt
hadoop fs -ls /myinput
```

   * Run the MapReduce job (mapper.py, reducer.py):

```
chmod +x mapper.py
chmod +x reducer.py
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar\
  -input /myinput\
  -output /myoutput\
  -mapper /home/hadoop/Lab07/mapper.py\
  -reducer /home/hadoop/Lab07/reducer.py 
```

   * If you want to re-run the job and the output directory already exists, delete it with: `hadoop fs -rm -r /myoutput`

   * Check results:

```
hadoop fs -ls /myoutput
hadoop fs -cat /myoutput/part-00000
```

## Stopping Hadoop

```
su hadoop
stop-yarn.sh
stop-dfs.sh
exit
```

## Deleting All Hadoop Data

Make sure you are user gb760. Then run:

```
sudo rm -rf /home/hadoop
sudo userdel hadoop
```
