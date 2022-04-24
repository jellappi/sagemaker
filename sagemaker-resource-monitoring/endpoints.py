import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_endpoint_state():

    endpoint_list = []

    for region in region_list:

        sagemaker = boto3.client('sagemaker', region_name=region)
        response_endpoints = sagemaker.list_endpoints()

        for endpoint in response_endpoints['Endpoints']:

            response = sagemaker.describe_endpoint(
                EndpointName=endpoint['EndpointName']
            )

            instance_count_list = []
            try:
                for variant in response['ProductionVariants']:
                    instance_count = variant['CurrentInstanceCount']
                    instance_count_list.append(instance_count)
            except:
                instance_count_list.append("No Instance Yet")

            response = sagemaker.describe_endpoint_config(
                EndpointConfigName=response['EndpointConfigName']
            )

            instance_type_list = []
            model_name_list = []
            try:
                for variant in response['ProductionVariants']:
                    instance_type_list.append(variant['InstanceType'])
                    model_name_list.append(variant['ModelName'])
            except:
                instance_type_list.append("No Instance Yet")
                model_name_list.append("No Model Yet")

            endpoint['CurrentInstanceCount'] = instance_count_list
            endpoint['InstanceType'] = instance_type_list
            endpoint['ModelName'] = model_name_list
            endpoint['Region'] = region

            endpoint_list.append(endpoint)

    return endpoint_list