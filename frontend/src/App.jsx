import { useState } from "react";

import "./App.css";

/*


This is the starting point of our application. Here, we can begin coding 
and transforming this page into whatever best suits our needs. 
For example, we can start by creating a login page, home page, or an about section; 
there are many ways to get your application up and running. 
With App.jsx, we can also define global variables and routes to store information as well as page navigation.
*/
function App() {

	const [video, setVideo] = useState(undefined);

    let onChangeHandler = (e) => {
        setVideo(e.target.files[0])
    };

    let onSubmitHandler = (e) => {
		// axios.post(url)
		console.log(video);
    };
	
	return (<div>
		<p className="instruction">Input a video:</p>
		<input type="file" accept=".mp4" className="button" onChange={onChangeHandler} />
		<div>
        	<input type="button" className="button submit-button" onClick={onSubmitHandler} value="Submit Video"/>
		</div>
	</div>)
}

export default App;
