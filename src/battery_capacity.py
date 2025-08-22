import os
import pandas as pd

data_dir = "data/raw_data"
results = []

for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(data_dir, file))

        # power ve enerji
        df["power_W"] = df["DC_Link_Voltage"] * df["DC_Link_Current"]
        df["energy_Wh"] = df["power_W"] / 3600  # dt ~1s kabul

        # toplam enerji (kWh)
        energy_total = df["energy_Wh"].sum() / 1000

        # SOC kolonunu seç
        soc_col = "PACK_Q_SOC_TRIMMED" if "PACK_Q_SOC_TRIMMED" in df.columns else "PACK_Q_SOC_INTERNAL"
        soc_start = df[soc_col].iloc[0]
        soc_end   = df[soc_col].iloc[-1]
        delta_soc = soc_start - soc_end

        if delta_soc > 1:  # en az %1 düşüş olsun
            capacity = energy_total / (delta_soc/100)
            results.append(capacity)
            print(f"{file}: {capacity:.2f} kWh")

if results:
    print("\nOrtalama kapasite:", sum(results)/len(results), "kWh")
