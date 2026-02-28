import "./App.css";
import VideoFeedback from "./components/VideoFeedback";
import logo from "./assets/testlogo.png";

function App() {
  return (
    <div className="min-h-screen bg-[#060D18] text-white flex flex-col">

      {/* ── Navbar ── */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/[0.07] backdrop-blur-xl bg-[#060D18]/75">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src={logo} alt="RedWings AI" className="h-8 w-auto object-contain" />
            <span className="font-display text-[1.3rem] tracking-[0.2em] text-white">
              REDWINGS <span className="text-[#E8112D]">AI</span>
            </span>
          </div>
          <span className="font-condensed text-[0.6rem] tracking-[0.35em] uppercase text-white/35 border border-white/[0.07] px-3 py-1.5 rounded-full">
            IrvineHacks 2026
          </span>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative pt-40 pb-20 px-6 text-center overflow-hidden">
        {/* Red glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-175 h-80 bg-[#E8112D] opacity-[0.09] blur-[120px] rounded-full pointer-events-none" />

        <div className="relative max-w-3xl mx-auto">
          <p className="font-condensed text-[0.6rem] tracking-[0.45em] uppercase text-[#E8112D] mb-5">
            ★ AI-Powered · Extreme Sports ★
          </p>
          <h1 className="font-display text-[clamp(3.5rem,10vw,7rem)] tracking-[0.06em] leading-[0.95] text-white mb-6">
            PUSH YOUR <span className="text-[#E8112D]">LIMITS</span><br />SAFELY
          </h1>
          <p className="font-body text-white/40 text-base leading-relaxed max-w-md mx-auto mb-10">
            Upload your trick footage. Get elite biomechanical analysis
            and AI coaching built for athletes who don't hold back.
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {["Pose Detection", "Injury Risk Score", "Form Corrections", "AI Coaching"].map((f) => (
              <span key={f} className="font-condensed text-[0.6rem] tracking-[0.25em] uppercase border border-white/[0.07] text-white/35 px-4 py-1.5 rounded-full">
                {f}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ── Divider ── */}
      <div className="flex items-center gap-3 max-w-sm mx-auto w-full px-6">
        <div className="flex-1 h-px bg-linear-to-r from-transparent to-[#E8112D]/40" />
        <div className="w-1.5 h-1.5 rounded-full bg-[#E8112D] shadow-[0_0_10px_rgba(232,17,45,0.6)]" />
        <div className="flex-1 h-px bg-linear-to-l from-transparent to-[#E8112D]/40" />
      </div>

      {/* ── Upload section ── */}
      <section className="max-w-3xl mx-auto w-full px-6 py-20">
        <span className="font-condensed text-[0.6rem] tracking-[0.4em] uppercase text-[#E8112D] block mb-1">
          Step 01
        </span>
        <h2 className="font-display text-[clamp(2rem,5vw,3rem)] tracking-[0.12em] text-white mb-2">
          ANALYZE YOUR MOVEMENT
        </h2>
        <p className="font-body text-white/40 text-sm leading-relaxed max-w-lg mb-8">
          Drop in a video of your trick or training run. Our computer vision pipeline
          extracts joint angles and impact data — then our AI coach turns it into actionable advice.
        </p>

        {/* VideoFeedback card — teammate's component untouched */}
        <div className="bg-white/2.5 border border-white/[0.07] rounded-2xl p-10 hover:border-[#E8112D]/25 transition-colors duration-300">
          <VideoFeedback />
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="max-w-3xl mx-auto w-full px-6 pb-24">
        <h3 className="font-display text-sm tracking-[0.4em] text-white/30 text-center mb-8">
          HOW IT WORKS
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-y md:divide-y-0 divide-white/[0.07] border border-white/[0.07] rounded-2xl overflow-hidden">
          {[
            { n: "01", icon: "🎬", label: "Upload",  desc: "Submit a video of your trick or training session" },
            { n: "02", icon: "🦴", label: "Detect",  desc: "MediaPipe extracts pose and joint angles frame by frame" },
            { n: "03", icon: "⚡", label: "Analyze", desc: "Risk engine scores your form and flags asymmetries" },
            { n: "04", icon: "🎯", label: "Coach",   desc: "GPT-4o generates personalized corrections and drills" },
          ].map(({ n, icon, label, desc }) => (
            <div key={n} className="bg-[#0b1525] hover:bg-[#E8112D]/4 transition-colors duration-200 p-6 flex flex-col gap-2">
              <span className="font-display text-xs tracking-[0.2em] text-[#E8112D]">{n}</span>
              <span className="text-2xl">{icon}</span>
              <p className="font-condensed text-xs tracking-[0.15em] uppercase text-white font-semibold">{label}</p>
              <p className="font-body text-xs text-white/35 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="mt-auto border-t border-white/[0.07] py-10 text-center">
        <p className="font-condensed text-[0.55rem] tracking-[0.45em] uppercase text-white/15">
          RedWings AI · IrvineHacks 2026 · Powered by MediaPipe + OpenAI
        </p>
      </footer>

    </div>
  );
}

export default App;