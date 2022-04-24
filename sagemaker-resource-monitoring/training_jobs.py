import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_training_job_state():
    
    training_job_list = [] 
    
    for region in region_list:
        
        sagemaker = boto3.client('sagemaker', region_name=region)
        
        training_jobs = sagemaker.list_training_jobs() 
        
        for job in training_jobs['TrainingJobSummaries']:
            if job['TrainingJobStatus'] == 'InProgress':
                job['Region'] = region
                training_job_list.append(job) 
            
    return training_job_list