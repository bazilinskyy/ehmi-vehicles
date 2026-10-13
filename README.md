# eHMIs on vehicles in India and the Netherlands

Online study of how pedestrians in India and the Netherlands read external human-machine interfaces (eHMIs) on vehicles. Participants view photos of a car, bus, truck or tuk-tuk approaching at 10 or 20 m, taken in India and in the Netherlands, with no eHMI or with one of these eHMIs: English text (WALK / STOP), text in the local language (Chaliye / Rukiye in Hindi, Lopen in Dutch), a green or red symbol, or a green or red light bar. After each photo they rate on 0-100 sliders whether they would cross, how safe they feel, how clear the message is and how quickly they understand the vehicle's intent. Eye gaze is recorded with the webcam (WebGazer). The study ends with a questionnaire on eHMI preferences. A collaboration of TU/e and IIT Indore.

## Experiment
The experiment runs on [jsPsych](https://www.jspsych.org) with a Node.js server that stores data in MongoDB. It is in `public/views/experiment.html`; the 136 stimuli and their conditions are in `public/img/stimuli_masked/` (number plates masked) and `public/img/stimuli_masked/mapping.csv`. Each participant sees a random subset of the stimuli (`n_images_per_participant`).

Run locally with `npm install` and `CONNECTION='<MongoDB connection string>' node app.js`, then open http://localhost:3000. URL parameters: `debug=true`, `save_data=false`, `eye_tracking=false`.

## Analysis
Export the data from MongoDB to JSON (`mongoexport --collection entries --type json --out heroku_0.json`), then run:

```
pip install pandas numpy matplotlib
python analysis/analyse.py <folder with heroku_*.json>
```

Per-participant tables (participants, answers per image, post-experiment questionnaire) are saved to `_output/` and are not in git, as they hold personal data. Figures are saved to `figures/`; the per-stimulus gaze heatmaps go to `figures/gaze/` and the script refreshes their table in this README. Ratings are averaged within each participant first, then across participants. Gaze data of a participant counts as invalid when fewer than half of the samples are distinct points (frozen gaze). Frozen gaze occurred in Firefox and Chrome. The experiment therefore keeps the webcam video rendered during image trials and restarts the camera after 15 identical consecutive gaze samples (about 0.5 s). Each image trial stores the number of restarts in `gaze_camera_restarts`; the participant table reports their sum.

## Results
Preliminary: N = 2 participants (data from 13 October 2026; both living in India, one stopped after 28 of 34 images). The figures are rebuilt by the analysis script as data comes in.

### Ratings by eHMI
![Ratings by eHMI](figures/ratings_by_ehmi.png)

### Ratings by vehicle and distance
![Ratings by vehicle and distance](figures/ratings_by_vehicle_distance.png)

### Ratings by country of the footage and of participants
![Ratings by country](figures/ratings_by_country.png)

### Post-experiment questionnaire
![Post-experiment questionnaire](figures/post_questionnaire.png)

### Eye gaze
![Gaze heatmap](figures/gaze_heatmap.png)

### Eye gaze per stimulus
<!-- gaze-per-stimulus:start -->
Gaze (orange, stronger = more) over each stimulus, from the 1 participant with valid gaze data. 28 of 136 stimuli have gaze data so far; n is the number of participants per stimulus.

<table>
<tr><td width="33%"><img src="figures/gaze/image_8.jpg" alt="Gaze on image 8"><br><sub>Image 8: India, Car, Text local: Chaliye, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_10.jpg" alt="Gaze on image 10"><br><sub>Image 10: India, Car, Text English: STOP, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_14.jpg" alt="Gaze on image 14"><br><sub>Image 14: India, Car, No eHMI, 20 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_18.jpg" alt="Gaze on image 18"><br><sub>Image 18: India, Bus, Text local: stop (Rukiye), 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_22.jpg" alt="Gaze on image 22"><br><sub>Image 22: India, Truck, Symbol green, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_26.jpg" alt="Gaze on image 26"><br><sub>Image 26: India, Truck, Text English: STOP, 10 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_33.jpg" alt="Gaze on image 33"><br><sub>Image 33: India, Truck, Symbol red, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_35.jpg" alt="Gaze on image 35"><br><sub>Image 35: India, Truck, No eHMI, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_40.jpg" alt="Gaze on image 40"><br><sub>Image 40: India, Tuk-Tuk, Symbol red, 10 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_54.jpg" alt="Gaze on image 54"><br><sub>Image 54: India, Bus, Light bar green, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_59.jpg" alt="Gaze on image 59"><br><sub>Image 59: India, Bus, Symbol red, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_64.jpg" alt="Gaze on image 64"><br><sub>Image 64: India, Car, Light bar red, 20 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_65.jpg" alt="Gaze on image 65"><br><sub>Image 65: India, Truck, Light bar green, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_67.jpg" alt="Gaze on image 67"><br><sub>Image 67: India, Truck, Light bar green, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_68.jpg" alt="Gaze on image 68"><br><sub>Image 68: India, Truck, Light bar red, 20 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_73.jpg" alt="Gaze on image 73"><br><sub>Image 73: NL, Bus, No eHMI, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_79.jpg" alt="Gaze on image 79"><br><sub>Image 79: NL, Bus, Text English: STOP, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_80.jpg" alt="Gaze on image 80"><br><sub>Image 80: NL, Bus, Text English: WALK, 10 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_86.jpg" alt="Gaze on image 86"><br><sub>Image 86: NL, Bus, Light bar red, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_90.jpg" alt="Gaze on image 90"><br><sub>Image 90: NL, Car, Light bar green, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_92.jpg" alt="Gaze on image 92"><br><sub>Image 92: NL, Car, Text local: Lopen, 10 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_99.jpg" alt="Gaze on image 99"><br><sub>Image 99: NL, Car, Symbol green, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_103.jpg" alt="Gaze on image 103"><br><sub>Image 103: NL, Car, Text English: STOP, 20 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_105.jpg" alt="Gaze on image 105"><br><sub>Image 105: NL, Truck, No eHMI, 10 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_126.jpg" alt="Gaze on image 126"><br><sub>Image 126: NL, Tuk-Tuk, Symbol green, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_128.jpg" alt="Gaze on image 128"><br><sub>Image 128: NL, Tuk-Tuk, Text English: WALK, 10 m (n = 1)</sub></td><td width="33%"><img src="figures/gaze/image_132.jpg" alt="Gaze on image 132"><br><sub>Image 132: NL, Tuk-Tuk, Light bar red, 20 m (n = 1)</sub></td></tr>
<tr><td width="33%"><img src="figures/gaze/image_136.jpg" alt="Gaze on image 136"><br><sub>Image 136: NL, Tuk-Tuk, Text English: WALK, 20 m (n = 1)</sub></td></tr>
</table>
<!-- gaze-per-stimulus:end -->
