export default function Navbar({ currentStep, onStepClick }) {
  const steps = ["PROFILE", "ANALYZE", "RESULTS"];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 backdrop-blur-md bg-black/60">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-9 h-9 bg-[#E8112D] rounded-full flex items-center justify-center shadow-[0_0_16px_rgba(232,17,45,0.5)]">
              <svg viewBox="0 0 24 24" fill="white" className="w-4 h-4">
                <path d="M12 2L8 8H2l5 4-2 7 7-4 7 4-2-7 5-4h-6z" />
              </svg>
            </div>
          </div>
          <div className="leading-none">
            <span className="font-display text-white text-xl tracking-[0.2em]">REDWINGS</span>
            <span className="text-[#E8112D] font-display text-xl tracking-[0.2em]"> AI</span>
          </div>
        </div>

        {/* Step pills */}
        <div className="flex items-center gap-1">
          {steps.map((step, i) => (
            <button
              key={step}
              onClick={() => onStepClick?.(i)}
              className={`px-4 py-1.5 rounded-full text-xs font-condensed tracking-widest uppercase transition-all duration-300 ${
                currentStep === i
                  ? "bg-[#E8112D] text-white shadow-[0_0_12px_rgba(232,17,45,0.4)]"
                  : currentStep > i
                  ? "bg-white/10 text-white/70 hover:bg-white/15 cursor-pointer"
                  : "bg-transparent text-white/30 cursor-default"
              }`}
              disabled={currentStep < i}
            >
              {currentStep > i ? "✓ " : `${i + 1}. `}{step}
            </button>
          ))}
        </div>

        {/* Tag */}
        <div className="hidden md:block text-right">
          <p className="text-[10px] font-condensed tracking-[0.3em] text-white/30 uppercase">IrvineHacks 2026</p>
        </div>
      </div>
    </nav>
  );
}
