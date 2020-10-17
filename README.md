# Mask Detection

<img src="1_huh2tZKYK3TwAulj_kUUqg.jpeg" width="300"/> 

## Details about this repo

Please read my article [here](https://medium.com/@harshshrm94/mask-detection-using-deep-learning-2958503d42b1), which has an explanation about how to detect mask given a video feed

## How To Use
* Clone this repo.
* Create the conda environment using the following command :
```
conda env create -n social_distancing -f environment.yml
```
* Activate the conda environment using the following command:
```
conda activate social_distancing
```
* Now you have to run the python file run.py with arguments video-path and save-path those indicate the location of the video you want to infer on and the location of the output you want to save in, respectively. You have to run the command :
```
python run.py --video-path 'location of video' --save-path 'save location with output video name'

```
