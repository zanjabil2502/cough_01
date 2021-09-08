# Decoding hidden patterns in COVID-19 coughs with AI

<p align="center"><img src="https://github.com/virufy/virufy-covid/blob/main/img/virufy-logo.png" alt="virufy logo" width="400"/></p>

Virufy is a nonprofit research organization developing artificial intelligence (AI) technology to screen for COVID-19 from cough patterns, rapidly and at no cost through use of a smartphone. To learn more or get involved, visit [our website](https://virufy.org/en/). For more information, check out the [resources available here.](https://drive.google.com/drive/u/4/folders/1kONSI53BvAAd7TvgNGzNAP8dT-Oq3iW1)

This repository contains everything needed to get started on writing a COVID-19 detection model. The goal of the model is to take the cough audio files, as well as additional metadata about a patient if desired, to predict whether or not they are infected with COVID-19. 

The [virufy_cdf_quickstart.ipynb](/virufy_cdf_quickstart.ipynb) notebook contains the setup to download the dataset, filter the dataset to only labled entries, and prepare the data for training and testing. There are instructions included for saving your model as well.

Questions?  
Join our [Slack support workspace](https://join.slack.com/t/virufycovid/shared_invite/zt-p62lib8g-Uz8YoTujfp5sxC7frpeiPw)

## Virufy common data format

Virufy has defined a [standardized data format](https://docs.google.com/document/d/1Joj2bslHOPmQvs2SvOw4EnKYHAjC2F_kdpscgqMMA-I/edit) for COVID coughs.

### Datasets

This data has been standardized using Virufy's Common Data Format. More data will be added as it becomes available.
1. https://github.com/virufy/virufy-cdf-coughvid
2. https://github.com/virufy/virufy-cdf-india-clinical-1
3. https://github.com/virufy/virufy-cdf-coswara

### Column structure
| Column | Description|
|--------|------------|
| row | Row number of the data. |
| source | Source of the cough data. |
| patient_id | Unique identifier for the patient. |
| cough_detected | The probability that the audio file contains an actual cough submission. |
| audio_path | The file path to the audio file containing the patient's cough submission. All of the cough audio files are in the [cough folder.](/cough) |
| audio_type | Either cough or speech |
| age | The age of the patient. |
| biological_sex | The sex at birth of the patient. This can be `male`, `female`, or `NaN`. |
| reported_gender | The reported gender of the patient. |
| submission_date | Date the cough was submitted by the patient to Coughvid. |
| pcr_test_date | Date the PCR test for the presence of COVID-19 was taken. |
| pcr_result_date | Date the test result from the PCR test for the presence of COVID-19 was received. |
| respiratory_condition | Boolean indicator of whether or not the patient suffers from a respitory condition. |
| fever_or_muscle_pain | Boolean indicator of whether or not the patient was suffering from fever or muscle pain. |
| pcr_test_result | Result of the patient's PCR test for the presence of COVID-19. This can be `positive`, `negative`, `untested`, or `pending`. |
| pcr_test_result_inferred | This is the best guess of a patient's COVID-19 diagnosis based on information specific to the dataset source. This can be `positive`, `negative`, `untested`, or `pending`. |
| covid_symptoms | Boolean indicator of whether or not the patient was experiencing symptoms of COVID-19. |

Note: The audio files containing the cough submissions are from a variety of file extensions including:
* `.webm`
* `.ogg`
* `.mp3`
* `.m4a`
* `.wav`
