from datetime import datetime
from celery import shared_task
from .models import License, LicenseType, Package, MailLog
from django.utils import timezone
from licenses.notifications import EmailNotification
task_queue_list = {}

@shared_task
def check_licenses():
    print("Checking licenses...")
    print(f"Timezone: {timezone.now()}")
    active_licenses = License.objects.filter(expiration_datetime__gte=timezone.now())
    package_types = Package.get_choices()
    licenses_types = LicenseType.get_choices()
    print(f"Active licenses: {active_licenses.count()}")

    for license in active_licenses:
        if(license.id not in task_queue_list):
            print(f'adding license {license.id} to task queue list')
            task_queue_list[license.id] = {}
            queue_tasks(license)
        elif(task_queue_list[license.id]['expiration_datetime'] != license.expiration_datetime):
            print(f'updating license {license.id} in task queue list')
            queue_tasks(license)

        
        # days_left = (license.expiration_datetime - timezone.now()).days
        # print(f"Client: {license.client.client_name} - Package: {package_types[license.package][0]} - Expiration: {license.expiration_datetime} - days left {days_left}")
        pass

    for license_id, license in task_queue_list.items():
        print(f"License: {license_id} - Expiration: {license['expiration_datetime']}")
        for task in license['scheduled_tasks']:
            if(task['sent']): continue
            print(f"\tTask: {task['task']} - Schedule: {task['schedule']}")
        pass
    
    print("Sending mails...")
    for license_id, license in task_queue_list.items():
        for task in license['scheduled_tasks']:
            schedule = task['schedule']
            isInTime = schedule > timezone.now() - timezone.timedelta(minutes=5) and schedule < timezone.now() + timezone.timedelta(minutes=5)
            # print(f"Task: {task['task']} - Schedule: {schedule} - isInTime: {isInTime}")
            if(isInTime and not task['sent']):
                license = License.objects.get(id=license_id)
                task['sent'] = True
                context = {
                    'license_id': license.id,
                    'license_type': licenses_types[license.license_type][0],
                    'license_package': package_types[license.package][0],
                    'license_expiration': license.expiration_datetime,
                    'poc_name': license.client.poc_contact_name,
                    'poc_email': license.client.poc_contact_email
                }
                print(f"Sending mail for task {task['task']}")
                mail_log = MailLog.objects.create(
                    license=license,
                    sent_datetime=timezone.now(),
                    reason=task['task']
                )
                mail_log.save()
                EmailNotification.send_notification([license.client.admin_poc.email], context)

def next_monday(date : datetime) -> datetime:
    """
    Get the next monday from a given date
    """
    days_ahead = 0 - date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return date + timezone.timedelta(days_ahead)

def queue_tasks(license: License):
    task_queue_list[license.id]['expiration_datetime'] = license.expiration_datetime
    _120_days_before_expiration = license.expiration_datetime - timezone.timedelta(days=120)
    _30_days_before_expiration = license.expiration_datetime - timezone.timedelta(days=30)
    month_left_and_monday = next_monday(_30_days_before_expiration)
    _7_days_before_expiration = license.expiration_datetime - timezone.timedelta(days=7)

    tasks_to_schedule = []
    if(_120_days_before_expiration > timezone.now()):
        tasks_to_schedule.append({'task': 'licenses.tasks.license_120_days_before_expiration', 'schedule': _120_days_before_expiration, 'sent': False})
    # if(_30_days_before_expiration > timezone.now()):
    #     tasks_to_schedule.append({'task': 'licenses.tasks.license_30_days_before_expiration', 'schedule': _30_days_before_expiration, 'sent': False'})
    if(month_left_and_monday > timezone.now()):
        tasks_to_schedule.append({'task': 'licenses.tasks.license_month_left_and_monday', 'schedule': month_left_and_monday, 'sent': False})
    if(_7_days_before_expiration > timezone.now()):
        tasks_to_schedule.append({'task': 'licenses.tasks.license_7_days_before_expiration', 'schedule': _7_days_before_expiration, 'sent': False})
    
    task_queue_list[license.id]['scheduled_tasks'] = tasks_to_schedule
    pass