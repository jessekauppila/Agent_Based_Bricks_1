def convert_to_hh_mm(total_minutes):
    minutes = total_minutes % 60
    return f"{minutes:02d}"

# Convert 9 hours to HH:MM format
minutes = 75
print(convert_to_hh_mm(minutes))  # Output: 09:00
