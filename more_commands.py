#!/usr/bin/env python3
import redis
from redis.exceptions import WatchError

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def more_redis(r):
    try:
   
        print("Setting key1:val1 on db")
        r.set("key1", "val1")

        print("Retrieving key1 from db:")
        msg = r.get("key1")
        print(msg)

        print("Bulk operations")
        # pipelines ensure the buffered commands are executed atomically as a group.
        # to deactivate this feature, use r.pipeline(transaction=False)
        pipe = r.pipeline()

        for key,val in zip(["key2", "key3", "key4"], ["val2", "val3", "val4"]):
            print(key, val)
            pipe.set(key, val)
        for key in ["key2", "key3", "key4"]:
            pipe.get(key)
        # The EXECUTE call sends all buffered commands to the server
        print(pipe.execute())

        print("Chaining operations")
        # INCR is an atomic operation
        print(pipe.set("count", "1").get("count").incr("count").get("count").execute())

    except Exception as e:
        print(e)

def first_atomic_implementation(r):

    """
    A common issue occurs when requiring atomic transactions but needing to retrieve values in Redis
    prior for use within the transaction.
    For instance, let’s assume that the INCR command didn’t exist
    and we need to build an atomic version of INCR in Python.
    WATCH provides the ability to monitor one or more keys prior to starting a transaction.
    If any of those keys change prior the execution of that transaction,
    the entire transaction will be canceled and a WatchError will be raised.
    To implement our own client-side INCR command, we could do something like this function
    """

    r.set('OUR-SEQUENCE-KEY', "1")

    with r.pipeline() as pipe:

        while True:
            try:
                # put a WATCH on the key that holds our sequence value
                pipe.watch('OUR-SEQUENCE-KEY')
                # after WATCHing, the pipeline is put into immediate execution
                # mode until we tell it to start buffering commands again.
                # this allows us to get the current value of our sequence
                current_value = pipe.get('OUR-SEQUENCE-KEY')
                next_value = int(current_value) + 1
                # now we can put the pipeline back into buffered mode with MULTI
                pipe.multi()
                pipe.set('OUR-SEQUENCE-KEY', next_value)
                # and finally, execute the pipeline (the set command)
                pipe.execute()
                # if a WatchError wasn't raised during execution, everything
                # we just did happened atomically.
                break

            except WatchError:
                # another client must have changed 'OUR-SEQUENCE-KEY' between
                # the time we started WATCHing it and the pipeline's execution.
                # our best bet is to just retry.
                continue

def second_atomic_implementation(pipe):

    """ A more friendly way to implement the previous operations, using 'transactions'."""    
    
    current_value = pipe.get('OUR-SEQUENCE-KEY')
    next_value = int(current_value) + 1
    pipe.multi()
    pipe.set('OUR-SEQUENCE-KEY', next_value)

if __name__ == '__main__':
    
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    more_redis(r)
    
    first_atomic_implementation(r)

    pipe = r.pipeline()   
    r.transaction(second_atomic_implementation, 'OUR-SEQUENCE-KEY') # func, *watches