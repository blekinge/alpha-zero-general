Installing cuda
---------------

First install cuda as a network install from

<https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1704&target_type=debnetwork>

Ie. download their deb package which sets up the apt repo.

The do
```bash
sudo dpkg -i cuda-repo-ubuntu1704_9.1.85-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1704/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda-9-0
```

When this is set up, you should fix the compiler links. Cuda require gcc 6 but ubuntu use gcc 7+ 

```bash
sudo ln -s /usr/bin/gcc-6 /usr/local/cuda-9.0/bin/gcc
sudo ln -s /usr/bin/g++-6 /usr/local/cuda-9.0/bin/g++
```

Then remove all old nvidia drivers (before nvidia-390), as they can interfere with Cuda

```bash
sudo apt remove nvidia-352
sudo apt autoremove
```

Then set up the paths and LD paths in `~/.bashrc`

```bash
#Cuda installation, https://developer.download.nvidia.com/compute/cuda/9.1/Prod/docs/sidebar/CUDA_Installation_Guide_Linux.pdf
export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```


**TODO is this nessesary?**

The NVIDIA Persistence Daemon can be started as the root user by running:

    /usr/bin/nvidia-persistenced --verbose

This command should be run on boot. Consult your Linux distribution's init
documentation for details on how to automate this.


Make samples to test everything works
=====================================

In order to modify, compile, and run the samples, the samples must be installed with
write permissions. A convenience installation script is provided:

    cuda-install-samples-9.0.sh <dir>

This script is installed with the cuda-samples-9-0 package. The cuda-samples-9-0
package installs only a read-only copy in /usr/local/cuda-9.0/samples.

Run 
    cuda-install-samples-9.0.sh ~/
to create a local copy of samples

You should compile them by changing to `~/NVIDIA_CUDA-9.0_Samples` and typing `make`. The
resulting binaries will be placed under `~/NVIDIA_CUDA-9.1_Samples/bin`.

After compilation, run `~/NVIDIA_CUDA-9.0_Samples/bin/x86_64/linux/release/deviceQuery` to see how
cuda recognizes your GFX card.


Install cuDNN
=============

Tensorflow require cuDNN, neural networks for cuda. Go to <https://developer.nvidia.com/rdp/cudnn-download> to download it.
You might have to sign up to NVidias developer program to get access, but this is free.

Then download **cuDNN 7.0.4 for CUDA 9.0**. Notice that the versions are IMPORTANT. The tensorflow version we are going
to install is compiled for **7.0.4** and we must use a cuDNN version that also match our installed CUDA version (9.0)

Download
[cuDNN v7.0.4 Runtime Library for Ubuntu16.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.4/prod/9.0_20171031/Ubuntu16_04-x64/libcudnn7_7.0.4.31-1+cuda9.0_amd64)
[cuDNN v7.0.4 Developer Library for Ubuntu16.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.4/prod/9.0_20171031/Ubuntu16_04-x64/libcudnn7-dev_7.0.4.31-1+cuda9.0_amd64)
[cuDNN v7.0.4 Code Samples and User Guide for Ubuntu16.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.4/prod/9.0_20171031/Ubuntu16_04-x64/libcudnn7-doc_7.0.4.31-1+cuda9.0_amd64)

Then install them with 
```bash
dpkg -i libcudnn7_7.0.4.31-1+cuda9.0_amd64.deb
dpkg -i libcudnn7-dev_7.0.4.31-1+cuda9.0_amd64.deb
dpkg -i libcudnn7-doc_7.0.4.31-1+cuda9.0_amd64.deb
```


Install Tensorflow
==================

Install the pip package `tensorflow-gpu==1.6.0` 