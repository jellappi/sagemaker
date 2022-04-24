import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_app_state():

    app_list = []

    for region in region_list:

        sagemaker = boto3.client('sagemaker', region_name=region)

        apps = sagemaker.list_apps()

        for app in apps["Apps"]:
            if app["Status"] != 'Deleted' and app['Status'] != 'Deleting' and app['AppType'] != 'JupyterServer':
                app['Region'] = region
                app_list.append(app)

    return app_list