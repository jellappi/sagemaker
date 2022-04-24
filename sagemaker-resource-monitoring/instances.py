import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_instance_state():

    instance_lists = []

    for region in region_list:

        sagemaker = boto3.client('sagemaker', region_name=region)

        instances = sagemaker.list_notebook_instances()

        for instance in instances["NotebookInstances"]:
            if instance["NotebookInstanceStatus"] == "InService" or instance["NotebookInstanceStatus"] == "Pending" or instance["NotebookInstanceStatus"] == "Updating":
                instance['Region'] = region
                instance_lists.append(instance)

    return instance_lists
