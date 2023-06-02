import time


def long_calculation(task_obj):
    
    for i in range(5):
        time.sleep(1)
        task_obj.update_state(state='PROGRESS', meta={"counter": i})
        
    return "result of long calculation"