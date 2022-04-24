import boto3

region_list = ['us-west-2', 'ap-northeast-2']


def check_schedule_state():
    
    schedule_list = []
    
    for region in region_list:
    
        sagemaker = boto3.client('sagemaker', region_name=region)
        
        schedules = sagemaker.list_monitoring_schedules() 
        
        for schedule in schedules['MonitoringScheduleSummaries']:
            schedule['Region'] = region
            schedule_list.append(schedule) 
            
    return schedule_list