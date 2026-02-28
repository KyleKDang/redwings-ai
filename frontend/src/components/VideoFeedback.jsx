import { useState } from "react";

import { getDataFromBackend } from "./Utils";

import axios from "axios"

import "./App.css";

function VideoFeedback({}) {
    const [video, setVideo] = useState(undefined);

	const [output, setOutput] = useState("");

    let onChangeHandler = (e) => {
        setVideo(e.target.files[0]);
    };

    let onSubmitHandler = async (e) => {
		if (video === undefined)
			return;

		// await axios.post("url", {
		// 	video: video
		// })

		setOutput("Working on it . . .");

		setTimeout(() => {setOutput("sample output")}, 5000);

		// setOutput(await axios.get("url"));

		// test GET request
		let data = await getDataFromBackend('random', {maximum: 100});
		console.log(data.itemId);

		console.log(video);
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