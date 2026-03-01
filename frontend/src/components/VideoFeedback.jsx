import { useState } from "react";
import axios from "axios";
import "../App.css";

function VideoFeedback({ profile, onResult }) {
    const [video, setVideo] = useState(undefined);
    const [output, setOutput] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const onChangeHandler = (e) => {
        setVideo(e.target.files[0]);
        setError("");
    };

    const onSubmitHandler = async () => {
        if (video === undefined) {
            setError("Please select a video first.");
            return;
        }
        if (!profile) {
            setError("Profile data is missing. Please complete your profile first.");
            return;
        }

        setLoading(true);
        setOutput("Working on it . . .");
        setError("");

        const data = new FormData();
        data.append("video", video);
        data.append("sport", profile.sport);
        data.append("skill_level", profile.skill_level);
        data.append("age", profile.age);
        data.append("height_cm", profile.height_ft * 30.48 + profile.height_in * 2.54);
        data.append("weight_kg", profile.weight_lbs / 2.205);
        data.append("fatigue_level", profile.fatigue_level);
        data.append("injury_history", profile.injury_history || "None");

        try {
            const response = await axios.post("/api/analyze", data);
            setOutput("");
            onResult(response.data); // pass result up to App
        } catch (err) {
            const msg = err.response?.data?.detail || "Something went wrong. Please try again.";
            setError(msg);
            setOutput("");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <p className="instruction">Input a video:</p>
            <input
                type="file"
                accept=".mp4"
                className="button"
                onChange={onChangeHandler}
                disabled={loading}
            />
            <div>
                <input
                    type="button"
                    className="button submit-button"
                    onClick={onSubmitHandler}
                    value={loading ? "Analyzing..." : "Submit Video"}
                    disabled={loading}
                />
            </div>
            {output && <p>{output}</p>}
            {error && <p style={{ color: "#E8112D" }}>{error}</p>}
        </div>
    );
}

export default VideoFeedback;