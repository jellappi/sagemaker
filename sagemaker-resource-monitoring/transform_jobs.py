import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_transform_job_state():
    
    transform_job_list = []
    
    for region in region_list:
    
        sagemaker = boto3.client('sagemaker', region_name=region)
        
        transform_jobs = sagemaker.list_transform_jobs() 
        
        for job in transform_jobs['TransformJobSummaries']:
            if job['TransformJobStatus'] == 'InProgress':
                job['Region'] = region
                transform_job_list.append(job) 
            
    return transform_job_list 