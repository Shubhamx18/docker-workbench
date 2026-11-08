# Docker Swarm Cheat Sheet

> **Swarm = Docker's built-in orchestrator.** You tell it *what you want* (e.g. "3 copies of nginx"), and Swarm keeps it that way.

**Key terms**

| Term | Meaning |
|---|---|
| **Node** | A machine in the swarm (manager or worker) |
| **Service** | The thing you want running (e.g. `web`) |
| **Task** | One running container of a service |
| **Replicas** | How many tasks (copies) you want |

---

## 1. Initialize the swarm

```bash
docker swarm init
```

If you get an error about **multiple network interfaces**, pass an address:

```bash
docker swarm init --advertise-addr 127.0.0.1          # single machine / practice
docker swarm init --advertise-addr 192.168.1.10       # your machine's real IP
```

> Use your real IP if you ever want to add other machines. `127.0.0.1` only works for a one-node setup.

**Check it worked**

```bash
docker info | grep -i swarm      # should say "Swarm: active"
docker node ls                   # lists nodes (you should see 1 Leader)
```

---

## 2. Create your first service

```bash
docker service create --name web --replicas 3 -p 8080:80 nginx
```

| Part | Meaning |
|---|---|
| `--name web` | name of the service |
| `--replicas 3` | run 3 copies |
| `-p 8080:80` | host port 8080 -> container port 80 |
| `nginx` | image to use |

**Check it**

```bash
docker service ls          # REPLICAS should show 3/3 when ready
docker service ps web      # shows the 3 tasks (all on your one node)
```

Open: http://localhost:8080

---

## 3. Self-healing

Swarm replaces any container that dies, so the replica count is always maintained.

```bash
docker ps                          # find a web container ID
docker rm -f <container_id>        # kill it
docker service ps web              # old task = Shutdown, new task = Running
```

---

## 4. Scaling

Three ways to change the number of replicas:

```bash
docker service scale web=5                 # scale up to 5
docker service scale web=2                 # scale down to 2
docker service update --replicas 4 web     # same thing, using update
```

---

## 5. Rolling update and rollback

**Update the image one container at a time (no downtime):**

```bash
docker service update \
  --image nginx:1.27 \
  --update-parallelism 1 \
  --update-delay 10s \
  web
```

| Flag | Meaning |
|---|---|
| `--update-parallelism 1` | update 1 task at a time |
| `--update-delay 10s` | wait 10 seconds between each task |

**Watch it happen**

```bash
docker service ps web
```

**Something broke? Go back to the previous version:**

```bash
docker service rollback web
```

---

## Extra commands (not in your notes, but useful)

**Inspect and debug**

```bash
docker service inspect --pretty web     # readable summary of the service
docker service logs web                 # logs from all tasks
docker service logs -f web              # follow logs live
```

**Remove and clean up**

```bash
docker service rm web                   # delete the service
docker swarm leave --force              # leave / destroy the swarm (practice only)
```

**Multi-node swarm**

```bash
docker swarm join-token worker          # prints the join command for a worker
docker swarm join-token manager         # same, for a manager
docker node promote <node>              # worker -> manager
docker node demote <node>               # manager -> worker
```

**Other service options**

```bash
docker service create --name web --mode global nginx     # exactly 1 task on every node
docker service update --publish-add 9090:80 web          # add a port
docker service update --env-add KEY=value web            # add an environment variable
```

**Deploy many services from a file (stack)**

```bash
docker stack deploy -c docker-compose.yml mystack    # deploy
docker stack ls                                      # list stacks
docker stack services mystack                        # services in a stack
docker stack rm mystack                              # remove
```

---

## Quick flow to remember

```
init -> create service -> check (ls / ps) -> kill one (self-heal)
     -> scale up/down -> rolling update -> rollback -> remove
```

## Quick fixes

| Problem | Fix |
|---|---|
| `could not choose an IP address to advertise` | Add `--advertise-addr <your-ip>` |
| Service stuck at `0/3` | `docker service ps web --no-trunc` to see the error |
| Port already in use | Change the host port, e.g. `-p 8081:80` |
| `This node is not a swarm manager` | Run the command on a manager node |
