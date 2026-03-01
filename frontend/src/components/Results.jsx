function MetricCard({ label, value, unit }) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4 text-center">
      <p className="font-condensed text-[0.55rem] tracking-[0.2em] uppercase text-white/30 mb-1">{label}</p>
      <p className="font-display text-2xl text-white">
        {typeof value === "number" ? value.toFixed(1) : "—"}
        {unit && <span className="text-xs text-white/30 ml-1">{unit}</span>}
      </p>
    </div>
  );
}

function BulletList({ items, icon, iconClass }) {
  return (
    <ul className="space-y-2">
      {items?.map((item, i) => (
        <li key={i} className="flex items-start gap-2 text-sm font-body text-white/70 leading-relaxed">
          <span className={`mt-0.5 flex-shrink-0 ${iconClass}`}>{icon}</span>
          {item}
        </li>
      ))}
    </ul>
  );
}

function SectionLabel({ children }) {
  return (
    <p className="font-condensed text-[1.2rem] tracking-[0.3em] uppercase text-white/40 mb-3">
      {children}
    </p>
  );
}

export default function Results({ result, onReset }) {
  const { coaching, metrics } = result;

  return (
    <section className="max-w-3xl mx-auto w-full px-6 pt-28 pb-20">

      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <span className="font-condensed text-[0.6rem] tracking-[0.4em] uppercase text-[#E8112D] block mb-1">
            Step 03
          </span>
          <h2 className="font-display text-[clamp(2rem,5vw,3rem)] tracking-[0.12em] text-white">
            YOUR REPORT
          </h2>
        </div>
        <button
          onClick={onReset}
          className="font-condensed text-[0.6rem] tracking-widest uppercase text-white/30 hover:text-white transition-colors mt-2"
        >
          ↩ Analyze another
        </button>
      </div>

      <div className="bg-white/[0.025] border border-white/[0.07] rounded-2xl p-8 space-y-6">

        {/* Overall assessment */}
        <div>
          <SectionLabel>Overall Assessment</SectionLabel>
          <p className="font-body text-white/70 text-sm leading-relaxed">{coaching?.overall_assessment}</p>
        </div>

        <div className="h-px bg-white/[0.07]" />

        {/* Coaching grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <SectionLabel>Form Corrections</SectionLabel>
            <BulletList items={coaching?.form_corrections} icon="▸" iconClass="text-[#E8112D]" />
          </div>
          <div>
            <SectionLabel>Safety Warnings</SectionLabel>
            <BulletList items={coaching?.safety_warnings} icon="⚠" iconClass="text-amber-400" />
          </div>
          <div>
            <SectionLabel>Recommended Drills</SectionLabel>
            <BulletList items={coaching?.drills} icon="▸" iconClass="text-[#E8112D]" />
          </div>
          <div>
            <SectionLabel>Conditioning</SectionLabel>
            <p className="text-sm font-body text-white/70 leading-relaxed">{coaching?.conditioning}</p>
          </div>
        </div>

        <div className="h-px bg-white/[0.07]" />

        {/* Metrics grid */}
        <div>
          <SectionLabel>Biomechanical Metrics</SectionLabel>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <MetricCard label="Knee Angle Avg"    value={metrics?.knee_angle_avg}     unit="°" />
            <MetricCard label="Knee Angle Min"    value={metrics?.knee_angle_min}     unit="°" />
            <MetricCard label="Knee Symmetry"     value={metrics?.knee_symmetry_avg}  unit="°" />
            <MetricCard label="Hip Angle Avg"     value={metrics?.hip_angle_avg}      unit="°" />
            <MetricCard label="Arm Spread Avg"    value={metrics?.arm_spread_avg}     unit=""  />
            <MetricCard label="Knee Velocity Max" value={metrics?.knee_velocity_max}  unit="°/f" />
          </div>
        </div>

      </div>
    </section>
  );
}