from .preprocessing import clean_irrigation_data, NUMERIC_COLUMNS


def irrigation_overview(data=None):
    data = clean_irrigation_data() if data is None else data
    return {
        'records': len(data),
        'classes': data['result'].value_counts().sort_index().to_dict(),
        'numeric_summary': data[NUMERIC_COLUMNS].describe().round(2)
    }
