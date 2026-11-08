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

## Missing from your notes (important ones only)

```bash
docker service logs web                 # see output/errors of a service
docker service inspect --pretty web     # readable details of a service
docker service rm web                   # delete the service (cleanup)
docker swarm leave --force              # leave the swarm (cleanup, practice only)
docker swarm join-token worker          # command to add another machine as a worker
```

---

## Flow to remember

```
init -> create service -> check (ls, ps) -> kill one (self-heal)
     -> scale up/down -> rolling update -> rollback -> remove
```
