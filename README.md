# README

Useful scripts to use redis and redis with python.

## Redis
Redis is a database engine in memory, based on the storage in hashes tables (key / value) but which can optionally be used as a durable or persistent database. To read more about persistance please visit: https://redis.io/topics/persistence.

## Installation
To install redis please visit: https://redis.io/topics/quickstart.<br>
To install redis library for python please visit: https://pypi.org/project/redis/.

## Tutorial
Nice dynamic tutorial of the redis-client : https://try.redis.io/.<br>
Official redis commands documentation: https://redis.io/commands.<br>
Nice tutorial of redis-py commands: https://pypi.org/project/redis/.

## Running Redis
Start the redis server typing from terminal:
```bash
<installation dir>/src/redis-server
```

To verify if redis server is working:
```bash
<installation dir>/src/redis-cli ping
```
The answer should be "PONG".

Run a redis client typing from terminal:
```bash
<installation dir>/src/redis-cli
```
and start coding. For example, to set a key:
```bash
set mykey somevalue
```

and to retrieve the key value:
```bash
get mykey
```

## Network Configuration
Configuration in file: `<installation dir>`/redis.conf

By default, if no "bind" configuration directive is specified, Redis listens
for connections from all the network interfaces available on the server.
It is possible to listen to just one or multiple selected interfaces using
the "bind" configuration directive, followed by one or more IP addresses.

Examples:

```
bind 192.168.1.100 10.0.0.1
bind 127.0.0.1 ::1
```

WARNING If the computer running Redis is directly exposed to the
internet, binding to all the interfaces is dangerous and will expose the
instance to everybody on the internet. So by default we uncomment the
following bind directive, that will force Redis to listen only into
the IPv4 loopback interface address (this means Redis will be able to
accept connections only from clients running into the same computer it
is running).

```
bind 127.0.0.1
```

Accept connections on the specified port, default is 6379 (IANA #815344).
If port 0 is specified Redis will not listen on a TCP socket.

```
port 6379
```

By default, password is set to "".


## Redis & Python
Please see the examples.

