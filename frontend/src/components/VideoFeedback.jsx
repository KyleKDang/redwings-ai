import { useState } from "react";

import { getDataFromBackend } from "../services/Utils";

import axios from "axios"

import "../App.css";

function VideoFeedback({profile}) {
    const [video, setVideo] = useState(undefined);

	const [output, setOutput] = useState("");

    let onChangeHandler = (e) => {
        setVideo(e.target.files[0]);
    };

    let onSubmitHandler = async (e) => {
		if (video === undefined)
			return;

		console.log(profile);

		setOutput("Working on it . . .");

		let data = new FormData();

		data.append("video", video);
		data.append("sport", profile.sport);
		data.append("skill_level", profile.skill_level);
		data.append("age", profile.age);
		data.append("height_cm", (profile.height_ft * 30.48 + profile.height_in * 2.54)); // ft, in to cm
		data.append("weight_kg", profile.weight_lbs / 2.205); // pounds to kg
		data.append("fatigue_level", profile.fatigue_level);
		data.append("injury_history", profile.injury_history);

		const response = await axios({
			method: "post",
			url: "/api/analyze",
			data: data
		});

		console.log(response);

		setOutput(response.data.coaching);
    };
	
	return (<div>
		<p className="instruction">Input a video:</p>
		<input type="file" accept=".mp4" className="button" onChange={onChangeHandler} />
		<div>
        	<input type="button" className="button submit-button" onClick={onSubmitHandler} value="Submit Video"/>
		</div>
		<p>
			{output}
		</p>
	</div>)
}

export default VideoFeedback;