import numpy as np
import pandas as pd

def estimate(d2, d1, t1):
    return (d2) * (t1 / d1)

# Given data
durations = np.array([1.02, 3.03, 5.01, 10.02, 20.01, 30.0, 40.02, 50.01, 60.0, 125.01, 280.02, 650.01, 1801.14])
time_taken = np.array([1.8068888187408447, 2.0778377056121826, 2.72623610496521, 2.912597179412842, 4.800200700759888, 
                       7.316509962081909, 8.122992753982544, 9.500887870788574, 13.072041273117065, 27.45095133781433, 
                       57.35416603088379, 135.15591168403625, 366.500568151474])

# Create table with NaN values (for better formatting)
table = np.full((len(durations), len(durations)), np.nan)

# Fill the lower triangle with estimated values
for i in range(len(durations)):
    for j in range(i):  # Only fill below diagonal
        table[i][j] = estimate(durations[i], durations[j], time_taken[j])

# Convert to pandas DataFrame
df = pd.DataFrame(table, index=[f"D={d:.2f}" for d in durations], columns=[f"D={d:.2f}" for d in durations])

# Add the actual time taken column
df["Actual Time Taken"] = time_taken

# Save to Excel
df.to_excel("Estimated_Times.xlsx")

print("Excel file 'Estimated_Times.xlsx' has been generated successfully!")
