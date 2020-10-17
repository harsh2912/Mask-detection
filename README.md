# Mask Detection

<img src="1_huh2tZKYK3TwAulj_kUUqg.jpeg" width="300"/> 

## Details about this repo

Please read my article [here](https://medium.com/@harshshrm94/mask-detection-using-deep-learning-2958503d42b1), which has an explanation about how to detect mask given a video feed

## How To Use
* Clone this repo.
* Download models from [here](https://drive.google.com/drive/folders/1G6-UJuLdDPybbk-4Z3829kQNzN8bhbIj?usp=sharing)
* Make a directory "models/retinaface" inside Face_detection folder and extract "retinaface-R50.zip" in that folder and maake a directory "model" inside Mask_classification folder and put "model_clean_data.pkl" in that folder.
* cd loc/Mask-detection/Face_detection
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
