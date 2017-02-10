import select
import psycopg2
import psycopg2.extensions
import constants as cons
import emailutil


def pg_listen():
    pid = []
    conn = cons.get_pg_conn()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = conn.cursor()
    curs.execute("LISTEN reset;")

    print ("Waiting for notifications on channel 'reset'")
    while 1:
        if select.select([conn],[],[],5) == ([],[],[]):
            print ("Timeout")
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print ("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
                if len(pid) == 100:
                    pid = []



                if not notify.pid in pid:
                    pid.append(notify.pid)
                    print("PID NOT FOUND",pid,notify.pid)
                # send email with link to reset the password
                    print("=========================================================")
                    if notify.channel == "reset":
                        emailutil.reset_password(notify.channel, notify.payload)
                






if __name__ == '__main__':
    pg_listen()
