import { useState } from "react";


const SPORTS = ["Snowboarding", "Skateboarding", "BMX", "Skiing", "Parkour", "Surfing", "Motocross", "Rock Climbing", "Wingsuiting", "Other"];
const SKILL_LEVELS = ["Beginner", "Intermediate", "Advanced", "Pro"];

function Field({ label, hint, children }) {
  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between">
        <label className="text-[15px] font-condensed tracking-[0.25em] uppercase text-white/50">{label}</label>
        {hint && <span className="text-[10px] text-white/25 font-body">{hint}</span>}
      </div>
      {children}
    </div>
  );
}

const inputCls =
  "w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-[#E8112D] focus:bg-white/[0.08] transition-all duration-200 font-body text-sm";

export default function ProfileForm({ onSubmit }) {
  const [form, setForm] = useState({
    sport: "Snowboarding",
    skill_level: "Intermediate",
    age: "",
    height_ft: "",
    height_in: "",
    weight_lbs: "",
    fatigue_level: 5,
    injury_history: "",
  });

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  return (
    <form
      onSubmit={(e) => { e.preventDefault(); onSubmit(form); }}
      className="space-y-6"
    >
      {/* Sport */}
      <Field label="Sport">
        <div className="flex flex-wrap gap-2">
          {SPORTS.map((s) => (
            <button
              key={s} type="button"
              onClick={() => set("sport", s)}
              className={`px-4 py-2 rounded-lg text-sm font-condensed tracking-wider uppercase transition-all duration-200 border ${
                form.sport === s
                  ? "bg-[#E8112D] border-[#E8112D] text-white shadow-[0_0_12px_rgba(232,17,45,0.35)]"
                  : "bg-white/5 border-white/10 text-white/60 hover:border-white/30 hover:text-white"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </Field>

      {/* Skill level */}
      <Field label="Skill Level">
        <div className="grid grid-cols-4 gap-2">
          {SKILL_LEVELS.map((lvl) => (
            <button
              key={lvl} type="button"
              onClick={() => set("skill_level", lvl)}
              className={`py-3 rounded-lg text-sm font-condensed tracking-wider uppercase transition-all duration-200 border ${
                form.skill_level === lvl
                  ? "bg-[#E8112D] border-[#E8112D] text-white shadow-[0_0_12px_rgba(232,17,45,0.35)]"
                  : "bg-white/5 border-white/10 text-white/60 hover:border-white/30 hover:text-white"
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>
      </Field>

      {/* Body metrics */}
      <div className="grid grid-cols-3 gap-4">
        <Field label="Age" hint="yrs">
          <input type="number" placeholder="24" min={10} max={80}
            value={form.age} onChange={(e) => set("age", e.target.value)}
            className={inputCls} required />
        </Field>
        <Field label="Height">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <input type="number" placeholder="5" min={3} max={8}
                value={form.height_ft} onChange={(e) => set("height_ft", e.target.value)}
                className={inputCls} required />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-white/30 font-condensed">ft</span>
            </div>
            <div className="relative flex-1">
              <input type="number" placeholder="10" min={0} max={11}
                value={form.height_in} onChange={(e) => set("height_in", e.target.value)}
                className={inputCls} required />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-white/30 font-condensed">in</span>
            </div>
          </div>
        </Field>
        <Field label="Weight" hint="lbs">
          <input type="number" placeholder="160"
            value={form.weight_lbs} onChange={(e) => set("weight_lbs", e.target.value)}
            className={inputCls} required />
        </Field>
      </div>

      {/* Fatigue slider */}
      <Field
        label={`Fatigue Level — ${form.fatigue_level} / 10`}
        hint={form.fatigue_level <= 3 ? "Feeling fresh" : form.fatigue_level <= 6 ? "Somewhat tired" : "Very fatigued"}
      >
        <div className="relative pt-1">
          <input
            type="range" min={1} max={10} value={form.fatigue_level}
            onChange={(e) => set("fatigue_level", parseInt(e.target.value))}
            className="w-full h-1 appearance-none bg-white/10 rounded-full accent-[#E8112D] cursor-pointer"
          />
          <div className="flex justify-between mt-2">
            {[1,2,3,4,5,6,7,8,9,10].map(n => (
              <div key={n} className={`w-1 h-1 rounded-full ${n <= form.fatigue_level ? "bg-[#E8112D]" : "bg-white/15"}`} />
            ))}
          </div>
        </div>
      </Field>

      {/* Injury history */}
      <Field label="Injury History" hint="optional">
        <textarea
          placeholder="e.g. Left knee sprain 2023, right ankle fracture 2022..."
          value={form.injury_history}
          onChange={(e) => set("injury_history", e.target.value)}
          rows={3}
          className={`${inputCls} resize-none`}
        />
      </Field>

      <button
        type="submit"
        className="w-full py-4 bg-[#E8112D] hover:bg-[#c50e26] text-white font-display text-2xl tracking-[0.3em] rounded-xl transition-all duration-200 hover:shadow-[0_0_30px_rgba(232,17,45,0.4)] hover:scale-[1.01] active:scale-[0.99]"
      >
        SAVE & CONTINUE →
      </button>
    </form>
  );
}
