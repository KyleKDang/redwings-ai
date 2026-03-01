import logo from "../assets/logo.png";

const steps = ["PROFILE", "ANALYZE", "RESULTS"];

export default function Navbar({ currentStep, onStepClick }) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/[0.07] backdrop-blur-xl bg-[#060D18]/80">
      <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">

        {/* Brand */}
        <div className="flex items-center gap-3">
          <img src={logo} alt="RedWings AI" className="h-8 w-auto object-contain" />
          <span className="font-display text-[1.2rem] tracking-[0.2em] text-white">
            REDWINGS <span className="text-[#E8112D]">AI</span>
          </span>
        </div>

        {/* Step pills */}
        <div className="flex items-center gap-1">
          {steps.map((step, i) => (
            <button
              key={step}
              onClick={() => onStepClick?.(i)}
              disabled={currentStep < i}
              className={`px-4 py-1.5 rounded-full font-condensed text-[0.65rem] tracking-widest uppercase transition-all duration-300 ${
                currentStep === i
                  ? "bg-[#E8112D] text-white shadow-[0_0_12px_rgba(232,17,45,0.4)]"
                  : currentStep > i
                  ? "bg-white/10 text-white/70 hover:bg-white/15 cursor-pointer"
                  : "bg-transparent text-white/25 cursor-default"
              }`}
            >
              {currentStep > i ? `✓ ${step}` : `${i + 1}. ${step}`}
            </button>
          ))}
        </div>

        {/* Tag */}
        <span className="hidden md:block font-condensed text-[0.6rem] tracking-[0.35em] uppercase text-white/25">
          IrvineHacks 2026
        </span>

      </div>
    </nav>
  );
}