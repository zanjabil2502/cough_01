1. Download dataset in this link:
https://www.kaggle.com/praveengovi/coronahack-respiratory-sound-dataset

2. Extract dataset on the same folder with this code
3. Run code "Dataset Process.ipynb"
4. The result of this code is a dataset of cough and talking sound (counting fast, counting normal, vowel-a,vowel-e, vowel-o) 
    you can download the result from this process at https://drive.google.com/file/d/1j6o7RrPlIwBbLWLgVq330e5fgJIbK5u1/view?usp=sharing
5. Run code "Split Dataset.ipynb" for split data to be train data, val data, and test data
6. Run code "Extracting MFCC.ipynb" for get features from audio and you will get data array in folder "array"
7. Run code "Training_validation_test.ipynb" for training model, validation model, test model
8. If you don't want training model, you can use file "cough_02.h5", where it accuration is 94%
9. Run code "Testing other data.ipynb" for test model using the other dataset
    you can download the other data for test model at https://drive.google.com/file/d/1t_hKa-XhzFMrFVdor0nIqMa2bTNkxjTd/view?usp=sharing