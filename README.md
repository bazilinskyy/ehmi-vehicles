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

Per-participant tables (participants, answers per image, post-experiment questionnaire) are saved to `_output/` and are not in git, as they hold personal data. Figures are saved to `figures/`. Ratings are averaged within each participant first, then across participants. Gaze data of a participant counts as invalid when fewer than half of the samples are distinct points (WebGazer did not track the face).

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
