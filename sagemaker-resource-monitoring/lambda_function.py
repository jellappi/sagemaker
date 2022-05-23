import boto3
import datetime
import apps
import instances
import endpoints
import monitoring_schedules
import training_jobs
import transform_jobs


def lambda_handler(event, context):
    # SES에 필요한 정보
    RECIPIENT = 'team@example.com'
    SENDER = 'team@example.com'
    SUBJECT = '[team] SageMaker 리소스 모니터링'

    # SES = boto3.client('ses', region_name = AWS_REGION)
    SES = boto3.client('ses')

    # 실행중인 app 리소스 정보 확인
    apps_lists = apps.check_app_state()

    if len(apps_lists) > 0:
        delete_app_lists = '''<h3>SageMaker Studio App 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>User</th>
        <th>Status</th>
        <th>Type</th>
        <th>Creation Time (KST)</th>
        </tr>'''

        for app in apps_lists:
            delete_app_lists += f'''<tr>
            <td>{app["AppName"]}</td>
            <td>{app["Region"]}</td>
            <td>{app["UserProfileName"]}</td>
            <td style="color:red;">{app['Status']}</td>
            <td>{app["AppType"]}</td>
            <td>{(app["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>'''

        delete_app_lists += "\n</table><br>"

    else:
        delete_app_lists = ''

    # 실행중인 instance 리소스 정보 확인
    instances_lists = instances.check_instance_state()

    if len(instances_lists) > 0:
        delete_instance_lists = '''<h3>SageMaker Instance 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>Type</th>
        <th>Status</th>
        <th>Creation Time (KST)</th>
        </tr>'''

        for instance in instances_lists:
            delete_instance_lists += f'''<tr>
            <td>{instance["NotebookInstanceName"]}</td>
            <td>{instance['Region']}</td>
            <td>{instance["InstanceType"]}</td>
            <td style="color:red;">{instance['NotebookInstanceStatus']}</td>
            <td>{(instance["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>'''

        delete_instance_lists += "\n</table><br>"

    else:
        delete_instance_lists = ''

    # 실행중인 endpoint 리소스 정보 확인
    endpoints_lists = endpoints.check_endpoint_state()

    if len(endpoints_lists) > 0:
        delete_endpoint_lists = '''<h3>SageMaker Endpoint 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>Status</th>
        <th>Creation Time (KST)</th>
        <th>Instance Count</th>
        <th>Instance Type</th>
        <th>Model Name</th>
        </tr>'''

        for endpoint in endpoints_lists:
            delete_endpoint_lists += f'''<tr>
            <td>{endpoint["EndpointName"]}</td>
            <td>{endpoint['Region']}</td>
            <td style="color:red;">{endpoint['EndpointStatus']}</td>
            <td>{(endpoint["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            <td>{endpoint['CurrentInstanceCount']}</td>
            <td>{endpoint['InstanceType']}</td>
            <td>{endpoint['ModelName']}</td>
            </tr>'''

        delete_endpoint_lists += "\n</table><br>"

    else:
        delete_endpoint_lists = ''

    # 실행중인 monitoring schedule 리소스 정보 확인
    schedules_lists = monitoring_schedules.check_schedule_state()

    if len(schedules_lists) > 0:
        delete_schedule_lists = '''<h3>SageMaker Monitoring Schedule 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>Status</th>
        <th>Endpoint Name</th>
        <th>Creation Time (KST)</th>
        </tr>'''

        for schedule in schedules_lists:
            delete_schedule_lists += f'''<tr>
            <td>{schedule["MonitoringScheduleName"]}</td>
            <td>{schedule["Region"]}</td>
            <td style="color:red;">{schedule['MonitoringScheduleStatus']}</td>
            <td>{schedule['EndpointName']}</td>
            <td>{(schedule["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>'''

        delete_schedule_lists += "\n</table><br>"

    else:
        delete_schedule_lists = ''

    # 실행중인 training job 리소스 정보 확인
    training_jobs_lists = training_jobs.check_training_job_state()

    if len(training_jobs_lists) > 0:
        delete_training_jobs_lists = '''<h3>SageMaker Training Job 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>Status</th>
        <th>Creation Time (KST)</th>
        </tr>'''

        for job in training_jobs_lists:
            delete_training_jobs_lists += f'''<tr>
            <td>{job["TrainingJobName"]}</td>
            <td>{job["Region"]}</td>
            <td style="color:red;">{job['TrainingJobStatus']}</td>
            <td>{(job["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>'''

        delete_training_jobs_lists += "\n</table><br>"

    else:
        delete_training_jobs_lists = ''

    # 실행중인 transform job 리소스 정보 확인
    transform_jobs_lists = transform_jobs.check_transform_job_state()

    if len(transform_jobs_lists) > 0:
        delete_transform_jobs_lists = '''<h3>SageMaker Transform Job 삭제 권고 </h3>
        <style>th,td {padding:10px;}</style>
        <table border="1">
        <tr>
        <th>Name</th>
        <th>Region</th>
        <th>Status</th>
        <th>Creation Time (KST)</th>
        </tr>'''

        for job in transform_jobs_lists:
            delete_transform_jobs_lists += f'''<tr>
            <td>{job["TransformJobName"]}</td>
            <td>{job["Region"]}</td>
            <td style="color:red;">{job['TransformJobStatus']}</td>
            <td>{(job["CreationTime"] + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>'''

        delete_transform_jobs_lists += "\n</table><br>"

    else:
        delete_transform_jobs_lists = ''

    BODY_HTML = f"""\
    <html>
    <head></head>
    <body>
    <h2>안녕하세요.<br> xxxx 본부 계정 담당자입니다.</h2>
    <p>본 메일은 자동으로 발송되는 메일로, 삭제가 필요한 SageMaker 리소스에 대해 모니터링 결과를 취합하여 전달드립니다.
    <br>
    아래 내용을 확인하시어 본인이 생성한 서비스에 대해 조치해주시기 바랍니다. </p>
    <hr>
    <br>
    {delete_app_lists}    <br>
    {delete_instance_lists}    <br>
    {delete_endpoint_lists}    <br>
    {delete_schedule_lists}    <br>
    {delete_training_jobs_lists}    <br>
    {delete_transform_jobs_lists}
    <hr>
    <h3>감사합니다.</h3>
    </body>
    </html>
    """

    # E-mail 전송
    len_whole_list = len(instances_lists) + len(apps_lists) + \
        len(endpoints_lists) + len(schedules_lists) + \
        len(training_jobs_lists) + len(transform_jobs_lists)
    if len_whole_list > 0:

        # E-mail 내용
        SES.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "utf-8",
                        'Data': BODY_HTML,
                    }
                },
                'Subject': {
                    'Charset': "utf-8",
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )

        return BODY_HTML
