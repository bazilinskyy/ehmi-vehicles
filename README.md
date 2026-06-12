# Analysing cross-cultural effects in viewing artworks

This project defines a framework for the analysis of cross-cultural effects in viewing artworks from Rijksmuseum, Amsterdam, the Netherlands. The jsPsych framework is used to for the frontend. In the description below, it is assumed that the repo is stored in the folder  art-crowdsourced`. Terminal commands lower assume macOS.

## Setup
Tested with Python 3.9.12. To setup the environment run these two commands in a parent folder of the downloaded repository (replace `/` with `\` and possibly add `--user` if on Windows):
- `pip install -e art-crowdsourced` will setup the project as a package accessible in the environment.
- `pip install -r art-crowdsourced/requirements.txt` will install required packages.

### Configuration of project
Configuration of the project needs to be defined in `art-crowdsourced/config`. Please use the `default.config` file for the required structure of the file. If no custom config file is provided, `default.config` is used. The config file has the following parameters:
* `appen_job`: ID of the appen job.
* `num_stimuli`: number of stimuli in the study.
* `num_stimuli_participant`: subset of stimuli in the study shown to each participant.
* `allowed_min_time`: the cut-off for minimal time of participation for filtering.
* `num_repeat`: number of times each stimulus is repeated.
* `mask_id`: number for masking worker IDs in appen data.
* `files_heroku`: files with data from heroku.
* `files_appen`: files with data from appen.
* `file_cheaters`: CSV file with cheaters for flagging.
* `path_stimuli`: path consisting of all videos included in the survey.
* `mapping_stimuli`: CSV file that contains all data found in the videos.
* `plotly_template`: template used to make graphs in the analysis.
* `stimulus_width`: width of stimuli.
* `stimulus_height`: height of stimuli.
* `freq`: frequency used by One Euro Filter.
* `mincutoff`: minimal cutoff used by One Euro Filter.
* `beta`: beta value used by One Euro Filter.
* `dcutoff`: d-cutoff value used by One Euro Filter.
* `font_family`: font family to be used on the figures.
* `font_size`: font size to be used on the figures.
* `p_value`: p value used for ttest.
* `save_figures`: save "final" figures to the /figures folder.

## Analysis
Analysis can be started by running python `art-crowdsourced/trust/run.py`. A number of CSV files used for data processing are saved in `art-crowdsourced/_output`. Visualisations of all data are saved in `art-crowdsourced/_output/figures/`.

### Heatmaps of eye gaze data
![image_1](figures/et_heatmap_image_1.png)  
Image 1.

![image_2](figures/et_heatmap_image_2.png)  
Image 2.

![image_3](figures/et_heatmap_image_3.png)  
Image 3.

![image_4](figures/et_heatmap_image_4.png)  
Image 4.

![image_5](figures/et_heatmap_image_5.png)  
Image 5.

![image_6](figures/et_heatmap_image_6.png)  
Image 6.

![image_7](figures/et_heatmap_image_7.png)  
Image 7.

![image_8](figures/et_heatmap_image_8.png)  
Image 8.

![image_9](figures/et_heatmap_image_9.png)  
Image 9.

![image_10](figures/et_heatmap_image_10.png)  
Image 10.

![image_11](figures/et_heatmap_image_11.png)  
Image 11.

![image_12](figures/et_heatmap_image_12.png)  
Image 12.

![image_13](figures/et_heatmap_image_13.png)  
Image 13.

![image_14](figures/et_heatmap_image_14.png)  
Image 14.

![image_15](figures/et_heatmap_image_15.png)  
Image 15.

![image_16](figures/et_heatmap_image_16.png)  
Image 16.

![image_17](figures/et_heatmap_image_17.png)  
Image 17.

![image_18](figures/et_heatmap_image_18.png)  
Image 18.

![image_19](figures/et_heatmap_image_19.png)  
Image 19.

![image_20](figures/et_heatmap_image_20.png)  
Image 20.

![image_21](figures/et_heatmap_image_21.png)  
Image 21.

![image_22](figures/et_heatmap_image_22.png)  
Image 22.

![image_23](figures/et_heatmap_image_23.png)  
Image 23.

![image_24](figures/et_heatmap_image_24.png)  
Image 24.

![image_25](figures/et_heatmap_image_25.png)  
Image 25.

![image_26](figures/et_heatmap_image_26.png)  
Image 26.

![image_27](figures/et_heatmap_image_27.png)  
Image 27.

![image_28](figures/et_heatmap_image_28.png)  
Image 28.

![image_29](figures/et_heatmap_image_29.png)  
Image 29.

![image_30](figures/et_heatmap_image_30.png)  
Image 30.

![image_31](figures/et_heatmap_image_31.png)  
Image 31.

![image_32](figures/et_heatmap_image_32.png)  
Image 32.

![image_33](figures/et_heatmap_image_33.png)  
Image 33.

![image_34](figures/et_heatmap_image_34.png)  
Image 34.

![image_35](figures/et_heatmap_image_35.png)  
Image 35.

![image_36](figures/et_heatmap_image_36.png)  
Image 36.

![image_37](figures/et_heatmap_image_37.png)  
Image 37.

![image_38](figures/et_heatmap_image_38.png)  
Image 38.

![image_39](figures/et_heatmap_image_39.png)  
Image 39.

![image_40](figures/et_heatmap_image_40.png)  
Image 40.

![image_41](figures/et_heatmap_image_41.png)  
Image 41.

<!-- #### Information on participants
[![driving frequency](figures/hist_driving_freq.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_driving_freq.html)  
Driving frequency.

[![mileage](figures/hist_milage.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_milage.html)  
Mileage.

[![input device](figures/hist_device.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_device.html)  
Input device.

[![driving behaviour questionnaire](figures/hist_dbq1_anger-dbq2_speed_motorway-dbq3_speed_residential-dbq4_headway-dbq5_traffic_lights-dbq6_horn-dbq7_mobile.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_dbq1_anger-dbq2_speed_motorway-dbq3_speed_residential-dbq4_headway-dbq5_traffic_lights-dbq6_horn-dbq7_mobile.html)  
Driving behaviour questionnaire (DBQ).

[![time of participation](figures/hist_time.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_time.html)  
Time of participation.

[![year of license](figures/hist_year_license.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_year_license.html)  
Year of obtaining driver's license.

[![education](figures/hist_education.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_education.html)  
Highest obtained level of education.

[![communication_others](figures/hist_communication_others.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_communication_others.html)  
Responses to statement "I would like to communicate with other road users while driving (for instance, using eye contact, gestures, verbal communication, etc.)".

[![technology](figures/hist_technology_worried-technology_enjoyment-technology_lives_easier-technology_lives_change-technology_not_interested.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_technology_worried-technology_enjoyment-technology_lives_easier-technology_lives_change-technology_not_interested.html)  
Technology acceptance scale.

[![machines](figures/scatter_machines_roles-machines_profit.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/scatter_machines_roles-machines_profit.html)  
Responses to x:"I enjoy making use of the latest technological products and services when I have the opportunity" and y:"New technologies are all about making profits rather than making people's lives better".

[![attitude AD](figures/hist_attitude_ad.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_attitude_ad.html)  
Responses to statement "Please indicate your general attitude towards automated cars".

[![driving with AD](figures/scatter_driving_in_ad-driving_alongside_ad.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/scatter_driving_in_ad-driving_alongside_ad.html)  
Responses to x:"When the autonomous vehicle is on the road, I would feel comfortable about driving on roads alongside autonomous cars" and y:"When the autonomous vehicle is on the road, I would feel comfortable about
using an autonomous car instead of driving a traditional car.".

[![capability of AD](figures/hist_capability_ad.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_capability_ad.html)  
Responses to question "Who do you think is more capable of conducting driving-related tasks?"

[![experience of AD](figures/hist_experience_ad.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/hist_experience_ad.html)  
Responses to question "Which options best describes your experience with automated cars?"

[![map of counts of participants](figures/map_counts.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/map_counts.html)  
Map of counts of participants.

[![map of years of having a license](figures/map_year_license.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/map_year_license.html)  
Map of years of having a license.

[![map of prediction of year of introduction of automated cars](figures/map_year_ad.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/map_year_ad.html)  
Map of prediction of the year of introduction of automated cars in the country of residence.

[![map of age](figures/map_age.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/map_age.html)  
Map of age of participants.

[![map of gender](figures/map_gender.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/map_gender.html)  
Map of distribution of gender. -->

<!-- #### Technical characteristics of participants
[![dimensions of browser](figures/scatter_window_width-window_height.png)](https://htmlpreview.github.io/?https://github.com/bazilinskyy art-crowdsourced/blob/main/figures/scatter_window_width-window_height.html)  
Dimensions of browser. -->

## Troubleshooting
### Troubleshooting setup
#### ERROR: art-crowdsourced is not a valid editable requirement
Check that you are indeed in the parent folder for running command `pip install -e art-crowdsourced`. This command will not work from inside of the folder containing the repo.