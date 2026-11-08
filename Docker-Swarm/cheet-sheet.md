# Docker Swarm Cheat Sheet

Swarm is Docker's built-in orchestrator. You say what you want (e.g. "3 copies of nginx") and Swarm keeps it that way.

**Terms:** Node = a machine in the swarm. Service = what you want running. Task = one running container of a service. Replicas = how many tasks.

---

## 1. Initialize

```bash
docker swarm init
```

Error about multiple network interfaces? Pass an address:

```bash
docker swarm init --advertise-addr 127.0.0.1        # single machine
docker swarm init --advertise-addr 192.168.1.10     # or your machine's IP
```

Check:

```bash
docker info | grep -i swarm      # Swarm: active
docker node ls                   # shows your node as Leader
```

---

## 2. First service

```bash
docker service create --name web --replicas 3 -p 8080:80 nginx
docker service ls                # replicas 3/3 when ready
docker service ps web            # 3 tasks, all on your one node
```

Test in browser or terminal: `http://localhost:8080` or `curl localhost:8080`

---

## 3. Self-healing

```bash
docker ps                        # find a web container ID
docker rm -f <container_id>      # kill it
docker service ps web            # old task = Shutdown, new task = Running
```

Swarm notices the missing replica and starts a new one automatically.

---

## 4. Scaling

```bash
docker service scale web=5
docker service scale web=2
docker service update --replicas 4 web
```

---

## 5. Rolling update and rollback

```bash
docker service update --image nginx:1.27 --update-parallelism 1 --update-delay 10s web
docker service ps web
docker service rollback web
```

- `--update-parallelism 1` : update 1 task at a time
- `--update-delay 10s` : wait 10 seconds between tasks
- `rollback` : goes back to the previous version

---

## 6. Other Useful Commands

### Check and debug

```bash
docker service ls                       # all services + replica count
docker service ps web                   # tasks of a service and their state
docker service ps web --no-trunc        # full error messages (use when a task fails)
docker service logs web                 # logs from all tasks of the service
docker service logs -f web              # follow logs live
docker service inspect --pretty web     # readable details (image, replicas, ports, update config)
```

### Nodes

```bash
docker node ls                          # list all nodes (run on a manager)
docker node inspect self --pretty       # details of the current node
docker swarm join-token worker          # prints the command to add a worker machine
docker swarm join-token manager         # prints the command to add a manager machine
```

Run the printed `docker swarm join ...` command on the other machine to add it.

### Change a running service

```bash
docker service update --publish-add 9090:80 web     # add a port
docker service update --publish-rm 9090 web         # remove a port
docker service update --env-add KEY=value web       # add an environment variable
```

### Cleanup

```bash
docker service rm web                   # delete the service (all its tasks stop)
docker swarm leave --force              # leave / destroy the swarm (practice only)
```

### Quick fixes

| Problem | Fix |
|---|---|
| `could not choose an IP address to advertise` | Add `--advertise-addr <your-ip>` to `docker swarm init` |
| Service stuck at `0/3` | `docker service ps web --no-trunc` to see the error |
| Port already in use | Use another host port, e.g. `-p 8081:80` |
| `This node is not a swarm manager` | Run the command on a manager node |

---

## Flow to remember

```
init -> create service -> check (ls, ps) -> kill one (self-heal)
     -> scale up/down -> rolling update -> rollback -> remove
```
