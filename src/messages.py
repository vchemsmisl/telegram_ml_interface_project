STARTING_MESSAGE_TRUE = '''
Welcome to the Simple ML Interface bot!
Let's begin.
'''
STARTING_MESSAGE_FALSE = 'Please enter "/start" or "/help" command!'
ASKING_FOR_DATASET_MESSAGE = '''
Send the dataset with features and target values.
Supported formats: .csv
File size must be not more than 20 MB.
Also please set the name of your target column to "target".
'''
WRONG_FILE_TYPE_MESSAGE = '''
Wrong file type! 
Send the file in one of the supported formats:
Supported formats: .csv 
'''
ASKING_FOR_TASK_TYPE_MESSAGE = '''
Now choose the type of task, for which the model will be trained.
'''
ASKING_FOR_TEST_PROPORTION_MESSAGE = '''
Now enter the proportion of test sample, which will be used for model validation.
Please enter the number from 0 to 1.
'''
WRONG_TEST_PROPORTION_MESSAGE = '''
Wrong number type! 
Please enter the number from 0 to 1.
'''
ASKING_FOR_MODELS_MESSAGE = '''
Now enter the names of machine learning models, which you want to use in AutoML algorithm.
Please write the names of models consequently, separating them by comma and space.

Possible variants are: 
1. lgb, 2. lgb_tuned, 3. linear_l2, 4. cb, 5. cb_tuned.
Otherwise, if you want AutoML to define working model based on your data, please enter "auto".
'''
WRONG_MODEL_NAME_MESSAGE = '''
One of the model names you entered is wrong! Please try again.

Possible variants are: 
1. lgb, 2. lgb_tuned, 3. linear_l2, 4. cb, 5. cb_tuned.
Otherwise, if you want AutoML to define working model based on your data, please enter "auto".
'''
ASKING_FOR_TIMEOUT_MESSAGE = '''
Now enter the number of timeout seconds.
Enter the non-negative integer number.
'''
WRONG_TIMEOUT_MESSAGE = '''
You entered a message of a wrong type!
Please enter the non-negative integer number.
'''
MODEL_TRAINING_START_MESSAGE = '''
Great! We have set all the necessary parameters and starting to train your AutoML model.
Now all you have to do is wait! The process will take several minutes.
When everything is ready, we will provide you with training results and a trained model.
'''
TRAINING_FINISHED_MESSAGE = '''
Congratulations!
We've just finished training AutoML model on your data.
In the following document you'll find the detailed report on model training.
'''