
import "./App.css";

import VideoFeedback from "./components/VideoFeedback"

import logo from "./assets/testlogo.png"

function App() {

	return <div>
		<h1>RedWings AI</h1>
		<img className="logo" src={logo}></img>
		<VideoFeedback />
	</div>
}

export default App;
