import { useState } from "react";

import axios from "axios"

import "./App.css";

import logo from "./assets/testlogo.png"

function VideoFeedback({}) {
    const [video, setVideo] = useState(undefined);

	const [output, setOutput] = useState(undefined);

    let onChangeHandler = (e) => {
        setVideo(e.target.files[0]);
    };

    let onSubmitHandler = (e) => {
		if (video === undefined)
			return;

		// await axios.post("url", {
		// 	video: video
		// })

		setOutput("Working on it . . .");

		setTimeout(() => {setOutput("sample output")}, 5000);

		// getDataFunc = async () => {
		// 	setOutput(await axios.get("url"))
		// }
		
		// getDataFunc();

		console.log(video);
    };
	
	return (<div>
		<p className="instruction">Input a video:</p>
		<input type="file" accept=".mp4" className="button" onChange={onChangeHandler} />
		<div>
        	<input type="button" className="button submit-button" onClick={onSubmitHandler} value="Submit Video"/>
		</div>
		<div>
			{output}
		</div>
	</div>)
}

export default VideoFeedback;