import pandas as pd
import os
from pathlib import Path

# Proje yolları
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw_data"
OUT_DIR  = BASE_DIR / "data"

all_files = sorted(RAW_DIR.glob("*.csv"))

dfs = [] #merge için df

for i, file in enumerate(all_files, start=1):
    # Dosya adını al
    filename = os.path.basename(file).replace(".csv","")

    # Sonda tekrar numarası varsa onu at
    if filename[-1].isdigit():
        scenario_name = filename[:-1]
    else:
        scenario_name = filename

    # Senaryo bilgisi
    speed = ''.join([c for c in scenario_name if c.isdigit()]) # 15, 25, 35
    load = "Loaded" if "L" in scenario_name else "Unloaded"
    direction = "CISAR" if "C" in scenario_name else "MMF"
    season = "Summer" if "S" in scenario_name else "Winter"

    df = pd.read_csv(file, sep=",")

    # Eklenecek sütunlar
    df["Experiment_ID"] = "Experiment_"+str(i)
    df["Average_Velocity"] = speed
    df["Load"] = load
    df["Direction"] = direction
    df["Season"] = season

    dfs.append(df)

ev_data = pd.concat(dfs, ignore_index=True)

out_csv = OUT_DIR / "ev_dataset.csv"
ev_data.to_csv(out_csv.as_posix(), index=False)



