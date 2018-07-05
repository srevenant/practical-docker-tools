# Fio benchmark container

Runs the fio benchmark tool in different configurations:

    docker-compose up --build

Look at Dockerfile, docker-compose.yml and bench.sh for more info.  You can also map a raw volume into the container for a baseline benchmark; cross-reference docker-compose.yml

## Results
When run on a MacBook Pro (with Filevault disk encryption enabled):

Two configs:

* Mac/D = Docker for mac (under xyhve VM), default config
* Mac/X = Docker for mac (under xyhve VM), [with flushing disabled](https://github.com/docker/for-mac/issues/668#issuecomment-284028148)
* Mac/F = Docker in Fedora in Parallels VM (with LVM/thinpool)

Three disk types:

* vol1-named = a named volume mount into the container, with `:cached` tuning
* vol2-bind = a bind volume mount from outside the container into the container, with `:cached` tuning
* vol3-local = using the "local" container layer


|                  | Mac/D       | Mac/X    | mac-f | 
|------------------|-------------|----------|-------|
| vol1-named read  | 4.1k IOPs   |          |       |
| vol1-named write | 13.9k IOPs  |          |       |
| vol2-bind read   | 482k IOPs   |          |       |
| vol2-bind write  | 12.2k IOPs  |          |       |
| vol3-local read  | 1,144k IOPs |          |       |
| vol3-local write | 7.9k IOPs   |          |       |
