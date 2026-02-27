# Docker Images

The [aind-ephys-pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) and the Geffen lab's [phy-export](./phy-export/phy-export.nf) pipeline are both based on Docker images.  These images are how we obtain processing code, along with all dependencies, in a versioned and reproducible way.

Some Docker images are large (multiple GB).
Here are some tips for managing them.

# Listing installed images

You can see which images are already installed by running `docker images`.  Here's an example from the cortex server:

```
$ docker images

IMAGE                                                                   ID             DISK USAGE   CONTENT SIZE   EXTRA
ghcr.io/allenneuraldynamics/aind-ephys-pipeline-base:si-0.103.0         7faa39e54024       11.3GB             0B        
ghcr.io/allenneuraldynamics/aind-ephys-pipeline-nwb:si-0.103.0          3e678f0fd275       1.83GB             0B        
ghcr.io/allenneuraldynamics/aind-ephys-spikesort-kilosort4:si-0.103.0   c0a7e5556b0a       10.9GB             0B        
ghcr.io/benjamin-heasly/geffenlab-bombcell:v0.0.2                       422d790d9966       3.13GB             0B        
ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.10            cd66f0e387a6       3.05GB             0B        
ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.11            8132d6fc9a7b       3.19GB             0B        
ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.5                    7c679a9d42d6       5.14GB             0B        
ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.10                7d588b664147       2.54GB             0B        
```

There are several images for `aind-ephys-pipeline` and several for `geffenlab`.
Each of these was downloaded automatically by Nextflow, the first time it was needed for a pipeline run.

Keeping the images on disk speeds up subsequent pipeline runs.
Otherwise, we'd have wait for the same images to be re-downloaded every time.

# Removing old images

Nextflow and Docker will keep images on disk indefinitely.
If you know that you no longer need an image, you must delete it manually.

For example, as we make fixes and improvements to pipeline steps we'll need to download newer versions of our images.
From time to time you can can delete older, stale image versions.

The listing above shows two versions of the same `geffenlab-ecephys-phy-export` image:

```
IMAGE                                                                   ID             DISK USAGE   CONTENT SIZE   EXTRA
ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.10            cd66f0e387a6       3.05GB             0B        
ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.11            8132d6fc9a7b       3.19GB             0B        
```

The older version, `v0.0.10`, is stale.  We can remove the image using its `ID` value from the listing, via `docker rmi`:

```
$ docker rmi cd66f0e387a6

Untagged: ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.10
Untagged: ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export@sha256:cef9874587a74ab7854cf48e17c83392cb6663c78b8047d1c96da83747a6fc76
Deleted: sha256:cd66f0e387a667a1aec1fe5e6dcefee38e65427df6194daf5c7c9f89aec070c9
Deleted: sha256:3099806e8166cec63d635d9b15513e15f89ca768a0a278e01eff0e584a0672aa
Deleted: sha256:5a6ad044c5c5f7f52fc60d8141a273aa38259fc2d59333c53580a009a7d67b0e
Deleted: sha256:704060bb51df1ab12fdc5affbc0d33bed763fb973c23c51307a7c3f7d3ac5468
Deleted: sha256:7ddfa130e3be570e16fd80044197c0858ca0f91862b3a50516907ba47355abe2
Deleted: sha256:780af30124af2160878ab2d3a3a9c184bf49356cd35a11bec429d98010c9a54a
Deleted: sha256:6ac5c802e9df5890e5d1f8ebad11775efcf9ec1ff97d6d406bdcdedaf85d496d
Deleted: sha256:f38c16bd6f32e14ae0b251eb2d83956c6ccb5db605fbbca6d61929da93b28bf0
```

Removing this one image would free up about 3GB of disk space.

## acceidentally removing required images

If you accidentally `docker rmi` an image that's needed for a pipeline, don't worry.
Nextflow will re-download the image the next time it's needed.

## `docker system prune`

`docker system prune` is another useful command that can free up space.
This tells Docker to find and remove unused containers and image layers.

Depending on what you've been doing with Docker this might free up a lot of space, or no space.
Either way, it should be harmless to run:

```
$ docker system prune

WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - unused build cache

Are you sure you want to continue? [y/N] y
Total reclaimed space: 0B
```

# Docker data in your home directory

On the cortex server, we use rootles Docker.
This is good because it means you can't use Docker to gain root access and accidentally break the system.

But, this also means that by default Docker stores image data within your home directory.
The images can consume much of your cortex home directory disk quota.
As of writing, the default quota was about 50GB and the Docker images listed above took up about 36GB -- most of the quota!

The default location for Docker image data is in your home directory at `~/.local/share/docker`.
You can check the size of this directory (or any directory!) with the `du` command:

```
$ du -d1 -h ~/.local/share/docker

4.0K    /home/ben/.local/share/docker/runtimes
36G     /home/ben/.local/share/docker/overlay2      <--- large
37M     /home/ben/.local/share/docker/image
8.0K    /home/ben/.local/share/docker/plugins
4.0K    /home/ben/.local/share/docker/containers
64K     /home/ben/.local/share/docker/network
4.0K    /home/ben/.local/share/docker/swarm
28K     /home/ben/.local/share/docker/volumes
4.0K    /home/ben/.local/share/docker/tmp
392K    /home/ben/.local/share/docker/containerd
108K    /home/ben/.local/share/docker/buildkit
37G     /home/ben/.local/share/docker
```

Note `36G` of images stored in `/home/ben/.local/share/docker/overlay2`.

# Moving the Docker data directory

You can configure your rootless Docker to save images and other data to a different location, outside of your home directory.
On cortex you can choose a location within `/vol/cortex/cd4/geffenlab/`.

## confirm the Docker data directory

First, confirm where Docker is storing data:

```
$ docker info | grep "Docker Root Dir"

Docker Root Dir: /home/ben/.local/share/docker
```

This confirms that Docker is saving images and other data within the user's home directory at `/home/ben/.local/share/docker`.

In this example the username is `ben`.
You must use your own username, instead.

## clean up existing images

Before moving to a new Docker data directory it can be helpful to clean up the current data directory.
You can do this with `docker system prune`.
Adding the `--all` flag asks Docker to clean up completely, instead of keeping some images.

```
$ docker system prune --all

WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all images without at least one container associated to them
  - all build cache

Are you sure you want to continue? [y/N] y
Total reclaimed space: 37GB
```

The first time you run this, it might free up a lot of space.
It will remove images that we want to use for pipelines, but Nextflow will automatically download these again as needed.
It will also remove any cruft that we don't need to move -- or can't move due to Docker-managed file permissions.

## stop Docker

Stop your Docker system process while the data move is happening.
With rootless Docker, this will only affect your cortex user, not anyone else.

```
$ systemctl --user stop docker
```

Confirm that docker is not running.  Try to run `docker images` again and expect an error like the following:

```
$ docker images

failed to connect to the docker API at unix:///run/user/10078/docker.sock; check if the path is correct and if the daemon is running: dial unix /run/user/10078/docker.sock: connect: no such file or directory
```

## move your Docker data directory

Create a new directory to hold your Docker images and other data.
A directory within `/vol/cortex/cd4/geffenlab/` won't count against your home directory quota.

Replace the username `ben` with your own cortex username.

```
$ mkdir -p /vol/cortex/cd4/geffenlab/docker-data/ben
```

Move your existing Docker data to the new location.

```
$ mv ~/.local/share/docker /vol/cortex/cd4/geffenlab/docker-data/ben/docker
```

## create a link from old location to new

Create a file system link from the old Docker data location to the new location.

```
$ ln -s /vol/cortex/cd4/geffenlab/docker-data/ben/docker ~/.local/share/docker
```

Docker will still look for `~/.local/share/docker` when it wants to store data.  But now, it will find that this is a link to the new location within `/vol/cortex/cd4/geffenlab`.

You can confirm the link with `ls`:

```
$ ls -alth ~/.local/share/docker

lrwxrwxrwx 1 ben geffenlab 48 Feb 27 15:29 /home/ben/.local/share/docker -> /vol/cortex/cd4/geffenlab/docker-data/ben/docker
```

## restart Docker

With the data moved and a link to the new location, Docker should be able to run again.
Restart your Docker system process.

```
$ systemctl --user start docker
```

Confirm that Docker can run its `hello-world` example.

```
$ docker run --rm hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
17eec7bbc9d7: Pull complete 
Digest: sha256:ef54e839ef541993b4e87f25e752f7cf4238fa55f017957c2eb44077083d7a6a
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

... etc ...
```

Docker should download its `hello-world` image and display a message like "Hello from Docker!".

## Confirm the new Docker data location

Finally, confirm that Docker is storing data in the new location:

```
$ docker info | grep "Docker Root Dir"
Docker Root Dir: /vol/cortex/cd4/geffenlab/docker-data/ben/docker
```

This confirms that Docker found the link from the old location to the new location, and is now saving images and other data within `/vol/cortex/cd4/geffenlab/docker-data/ben/docker`.

You should be able to list the image(s) in the new location:

```
$ docker images
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   1b44b5a3e06a       10.1kB             0B        
```

At first `hello-world` might be the only image present.

But now you should be ready to run pipelines again, and see those larger images saved outside of your home directory.
