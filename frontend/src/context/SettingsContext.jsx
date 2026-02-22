import { createContext, useContext, useMemo, useState } from "react";

const SettingsContext = createContext(null);

const DEFAULT_STATE = {
  filters: {
    ramp: false,
    powerDoors: false,
    elevator: false,
  },
  theme: {
    darkMode: false,
    highContrast: false,
  },
  units: "in", // "mm" or "in"
};

export function SettingsProvider({ children }) {
  const [state, setState] = useState(DEFAULT_STATE);

  const value = useMemo(
    () => ({
      state,
      toggleFilter: (key) =>
        setState((s) => ({
          ...s,
          filters: { ...s.filters, [key]: !s.filters[key] },
        })),
      setTheme: (key, value) =>
        setState((s) => ({
          ...s,
          theme: { ...s.theme, [key]: value },
        })),
      setUnits: (unit) =>
        setState((s) => ({
          ...s,
          units: unit,
        })),
      reset: () => setState(DEFAULT_STATE),
    }),
    [state]
  );

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>;
}

export function useSettings() {
  const ctx = useContext(SettingsContext);
  if (!ctx) throw new Error("useSettings must be used inside SettingsProvider");
  return ctx;
}
