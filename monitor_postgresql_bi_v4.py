#!/usr/bin/env python

try:
    import argparse
    import subprocess
    import configparser
    import smtplib
    import email.message
except ImportError:
    raise Exception('Missing Python3 modules')


def check_postgres(host, database_name, port, user, password, sqlfile):
    """
    Executes SQL query from a file.
    """
    try:
        process = subprocess.check_output(
            ['psql',
             '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password,
             host, port, database_name), 
             '--file={}'.format(sqlfile)]
        )
        all_statuses = process.decode(encoding='UTF-8').split('\n')[4].split('|')
        current_state = all_statuses[0].strip()
        last_state = all_statuses[1].strip()
        return current_state, last_state
    except Exception as e:
        print(e)
        exit(1)


def send_email(smtp_server, port, sender_email, sender, password, recepients,
               subject, email_body):
    """
    Sends HTML formatted email to one or more recepients.
    """
    msg = email.message.Message()
    msg.add_header('content-type', 'text/html')
    msg['subject'] = subject
    msg.set_payload(email_body)

    try: 
        s = smtplib.SMTP(smtp_server,port)
        s.ehlo()
        s.starttls()
        s.login(sender_email, password)
        rcpto = list(recepients.split(","))
        s.sendmail(sender, rcpto, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        s.quit()


def main():
    args_parser = argparse.ArgumentParser(description='Postgres database management')
    args_parser.add_argument("--configfile",
                             required=True,
                             help="Database configuration file")
    args = args_parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.configfile)

    postgres_host = config.get('postgresql', 'host')
    postgres_port = config.get('postgresql', 'port')
    postgres_db = config.get('postgresql', 'db')
    postgres_user = config.get('postgresql', 'user')
    postgres_password = config.get('postgresql', 'password')
    postgres_query_file = config.get('postgresql', 'file')
    smtp_server = config.get('smtp', 'smtp_server')
    smtp_port = config.get('smtp', 'port')
    smtp_sender_email = config.get('smtp', 'sender_email')
    smtp_sender = config.get('smtp', 'sender')
    smtp_password = config.get('smtp', 'password')
    smtp_recepients = config.get('smtp', 'recepients')
    smtp_subject_issue = config.get('smtp', 'subject_issue')
    smtp_subject_resolved = config.get('smtp', 'subject_resolved')
    smtp_body_issue = config.get('smtp', 'email_body_issue')
    smtp_body_resolved = config.get('smtp', 'email_body_resolved')

    current_state, last_state = check_postgres(postgres_host,
                            postgres_db,
                            postgres_port,
                            postgres_user,
                            postgres_password,
                            postgres_query_file)

    if last_state == "ERROR":
        if current_state == "OK":
            send_email(smtp_server,
                       smtp_port,
                       smtp_sender_email,
                       smtp_sender,
                       smtp_password,
                       smtp_recepients,
                       smtp_subject_resolved,
                       smtp_body_resolved)
        elif current_state == "ERROR":
            pass
    elif current_state == "ERROR":
        send_email(smtp_server,
                   smtp_port,
                   smtp_sender_email,
                   smtp_sender,
                   smtp_password,
                   smtp_recepients,
                   smtp_subject_issue,
                   smtp_body_issue)


if __name__ == '__main__':
    main()